import logging
import math
import re
from collections import Counter
from typing import Any, Dict, List, Optional
from src.repositories.chat_repository import chat_repository

logger = logging.getLogger(__name__)


def tokenize_vietnamese(text: str) -> List[str]:
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    words = clean.split()
    tokens = list(words)
    for i in range(len(words) - 1):
        tokens.append(f"{words[i]}_{words[i+1]}")
    return tokens


class BM25SearchEngine:
    def __init__(self, chunks: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.doc_len: List[int] = []
        self.inverted_index: Dict[str, Dict[int, int]] = {}
        self.doc_freqs: Counter = Counter()
        self.corpus_size: int = len(chunks)
        self.avg_len: float = 1.0
        self._build()

    def _build(self) -> None:
        if not self.corpus_size:
            return
        total = 0
        for doc_id, chunk in enumerate(self.chunks):
            breadcrumb = chunk.get("breadcrumb", "")
            section = chunk.get("section", "")
            content = chunk.get("content", "")
            full_txt = f"{breadcrumb} {section} {content}"
            toks = tokenize_vietnamese(full_txt)
            self.doc_len.append(len(toks))
            total += len(toks)
            tf = Counter(toks)
            for t, cnt in tf.items():
                if t not in self.inverted_index:
                    self.inverted_index[t] = {}
                self.inverted_index[t][doc_id] = cnt
                self.doc_freqs[t] += 1
        self.avg_len = (total / self.corpus_size) if self.corpus_size else 1.0

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.corpus_size:
            return []
        toks = tokenize_vietnamese(query)
        scores = [0.0] * self.corpus_size
        for t in toks:
            if t not in self.inverted_index:
                continue
            df = self.doc_freqs[t]
            idf = math.log(1 + (self.corpus_size - df + 0.5) / (df + 0.5))
            for doc_id, tf in self.inverted_index[t].items():
                dl = self.doc_len[doc_id]
                score = idf * (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (dl / self.avg_len)))
                scores[doc_id] += score

        ranked = sorted(range(self.corpus_size), key=lambda i: scores[i], reverse=True)
        results = []
        for i in ranked[:top_k]:
            if scores[i] > 0:
                item = dict(self.chunks[i])
                item["score"] = round(scores[i], 3)
                results.append(item)
        return results


class RAGPipeline:
    def __init__(self):
        self.all_chunks: List[Dict[str, Any]] = []
        self.engine: Optional[BM25SearchEngine] = None
        self._load_knowledge_from_db()

    def _convert_db_item_to_chunk(self, item: Dict[str, Any]) -> Dict[str, Any]:
        chu_de = item.get("chu_de") or "Tri thức UTC"
        cau_hoi = item.get("cau_hoi_mau") or ""
        noi_dung = item.get("noi_dung") or ""
        ma_tri_thuc = item.get("ma_tri_thuc") or ""

        if "st67" in ma_tri_thuc:
            doc_label = "Sổ tay Sinh viên K67"
        elif "ng64" in ma_tri_thuc:
            doc_label = "Niên giám Đào tạo K64"
        else:
            doc_label = f"Hỏi đáp Tuyển sinh - {chu_de}"

        return {
            "chunk_id": ma_tri_thuc,
            "doc_label": doc_label,
            "breadcrumb": chu_de,
            "section": cau_hoi,
            "page_range": "CSDL Tri thức AI",
            "content": noi_dung if not cau_hoi or cau_hoi in noi_dung else f"Câu hỏi: {cau_hoi}\nNội dung: {noi_dung}",
        }

    def _load_knowledge_from_db(self, db_items: Optional[List[Dict[str, Any]]] = None) -> None:
        if db_items is None:
            try:
                db_items = chat_repository.get_active_tri_thuc()
            except Exception as e:
                logger.error(f"Lỗi tải tri thức từ Supabase: {str(e)}")
                db_items = []

        chunks: List[Dict[str, Any]] = []
        for item in db_items:
            chunks.append(self._convert_db_item_to_chunk(item))

        self.all_chunks = chunks
        self.engine = BM25SearchEngine(self.all_chunks)
        logger.info(f"RAG Pipeline đã nạp {len(self.all_chunks)} mục tri thức từ CSDL Supabase.")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.engine:
            self._load_knowledge_from_db()
        if not self.engine:
            return []
        return self.engine.search(query, top_k=top_k)

    def reload(self, db_items: Optional[List[Dict[str, Any]]] = None) -> int:
        self._load_knowledge_from_db(db_items=db_items)
        return len(self.all_chunks)


rag_pipeline = RAGPipeline()
