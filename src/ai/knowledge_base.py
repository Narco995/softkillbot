"""Knowledge Base with Semantic Search & Vector DB Integration."""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib

from ..utils.logger import logger


@dataclass
class KnowledgeItem:
    """Item stored in knowledge base."""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    embedding: List[float]
    relevance_score: float
    created_at: datetime
    updated_at: datetime
    usage_count: int


class KnowledgeBase:
    """Semantic knowledge base with vector search capabilities."""

    def __init__(self):
        """Initialize knowledge base."""
        self.items: Dict[str, KnowledgeItem] = {}
        self.index: Dict[str, List[str]] = {}  # Tag-based inverted index
        self.clusters: Dict[str, List[str]] = {}  # Semantic clusters

    def add_knowledge(self, title: str, content: str, category: str, tags: List[str]) -> str:
        """Add knowledge item to base."""
        try:
            # Generate ID
            item_id = hashlib.md5(f"{title}{datetime.utcnow()}".encode()).hexdigest()[:8]

            # Generate embedding (in production, use real embedding model)
            embedding = self._generate_embedding(content)

            # Create item
            item = KnowledgeItem(
                id=item_id,
                title=title,
                content=content,
                category=category,
                tags=tags,
                embedding=embedding,
                relevance_score=1.0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                usage_count=0,
            )

            self.items[item_id] = item

            # Update indices
            self._update_indices(item_id, tags, category)

            logger.info(f"Knowledge item added: {title} ({item_id})")
            return item_id
        except Exception as e:
            logger.error(f"Error adding knowledge: {str(e)}")
            raise

    def semantic_search(self, query: str, top_k: int = 5) -> List[KnowledgeItem]:
        """Search knowledge base semantically."""
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)

            # Calculate similarity for all items
            similarities = []
            for item_id, item in self.items.items():
                similarity = self._cosine_similarity(
                    query_embedding,
                    item.embedding,
                )
                similarities.append((item_id, similarity, item))

            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Return top-k results
            results = [item for _, _, item in similarities[:top_k]]

            # Update usage count
            for result in results:
                result.usage_count += 1
                result.updated_at = datetime.utcnow()

            logger.info(f"Semantic search for '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []

    def find_similar_solutions(self, problem: str) -> List[KnowledgeItem]:
        """Find similar solutions from knowledge base."""
        # Use semantic search to find similar problems/solutions
        return self.semantic_search(problem)

    def recommend_patterns(self, task_context: Dict) -> List[Dict]:
        """Recommend design patterns based on task context."""
        try:
            recommendations = []

            # Convert context to query
            query = f"{task_context.get('task_type', '')} {task_context.get('requirements', '')}"

            # Search for similar patterns
            similar_items = self.semantic_search(query)

            for item in similar_items:
                recommendations.append(
                    {
                        "pattern": item.title,
                        "description": item.content,
                        "relevance": item.relevance_score,
                        "tags": item.tags,
                    }
                )

            return recommendations
        except Exception as e:
            logger.error(f"Error recommending patterns: {str(e)}")
            return []

    def cluster_by_context(self) -> Dict[str, List[str]]:
        """Cluster knowledge items by semantic context."""
        try:
            clusters = {}

            # Simple clustering based on tags
            for item_id, item in self.items.items():
                primary_tag = item.tags[0] if item.tags else "uncategorized"

                if primary_tag not in clusters:
                    clusters[primary_tag] = []

                clusters[primary_tag].append(item_id)

            self.clusters = clusters
            logger.info(f"Created {len(clusters)} semantic clusters")
            return clusters
        except Exception as e:
            logger.error(f"Error clustering knowledge: {str(e)}")
            return {}

    def get_usage_stats(self) -> Dict:
        """Get knowledge base usage statistics."""
        total_items = len(self.items)
        total_usages = sum(item.usage_count for item in self.items.values())
        avg_usage = total_usages / total_items if total_items > 0 else 0

        # Find most useful items
        top_items = sorted(
            self.items.values(),
            key=lambda x: x.usage_count,
            reverse=True,
        )[:5]

        return {
            "total_items": total_items,
            "total_usages": total_usages,
            "average_usage_per_item": avg_usage,
            "num_clusters": len(self.clusters),
            "top_items": [{
                "title": item.title,
                "usage_count": item.usage_count,
            } for item in top_items],
        }

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text (simulated)."""
        # In production, use OpenAI, Cohere, or local embedding model
        # This is a mock implementation
        import hashlib
        hash_val = hashlib.md5(text.encode()).digest()
        return [float(b) / 255.0 for b in hash_val[:16]]

    def _cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a ** 2 for a in embedding1) ** 0.5
        norm2 = sum(b ** 2 for b in embedding2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _update_indices(self, item_id: str, tags: List[str], category: str):
        """Update search indices."""
        # Update tag index
        for tag in tags:
            if tag not in self.index:
                self.index[tag] = []
            self.index[tag].append(item_id)

        # Update category index
        if category not in self.index:
            self.index[category] = []
        self.index[category].append(item_id)
