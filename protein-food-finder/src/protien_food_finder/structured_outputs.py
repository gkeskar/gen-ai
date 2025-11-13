"""Structured output models for protein food finder."""
from pydantic import BaseModel, Field
from typing import List, Optional


class Store(BaseModel):
    """Model for a grocery store."""
    name: str = Field(description="Store name")
    distance_miles: float = Field(description="Distance from location in miles")
    store_type: str = Field(description="Type of store (e.g., Trader Joe's, Costco, Indian grocery)")
    address: Optional[str] = Field(default=None, description="Store address if available")


class StoreList(BaseModel):
    """List of stores near the location."""
    stores: List[Store] = Field(description="List of grocery stores")


class ProteinProduct(BaseModel):
    """Model for a high-protein product."""
    product_name: str = Field(description="Product name")
    store: str = Field(description="Store where available")
    protein_grams: int = Field(description="Protein content in grams per serving")
    serving_size: Optional[str] = Field(default=None, description="Serving size (e.g., '1 cup', '3 oz')")
    price: Optional[float] = Field(default=None, description="Price in USD")
    category: str = Field(description="Category: dairy, plant-based, meat, seafood, supplements, whole-foods")
    calories: Optional[int] = Field(default=None, description="Calories per serving")
    total_fat_g: Optional[float] = Field(default=None, description="Total fat in grams")
    carbs_g: Optional[float] = Field(default=None, description="Carbohydrates in grams")
    fiber_g: Optional[float] = Field(default=None, description="Fiber in grams")
    sugar_g: Optional[float] = Field(default=None, description="Sugar in grams")
    is_gluten_free: Optional[bool] = Field(default=None, description="Whether product is gluten-free")
    contains_beef: Optional[bool] = Field(default=False, description="Contains beef")
    contains_pork: Optional[bool] = Field(default=False, description="Contains pork")
    notes: Optional[str] = Field(default=None, description="Additional notes or details")


class ProductList(BaseModel):
    """List of high-protein products organized by store."""
    products: List[ProteinProduct] = Field(description="List of high-protein products")

    def get_products_by_store(self, store_name: str) -> List[ProteinProduct]:
        """Get all products from a specific store."""
        return [p for p in self.products if p.store.lower() == store_name.lower()]

    def filter_by_dietary_preferences(self,
                                     exclude_beef: bool = True,
                                     exclude_pork: bool = True,
                                     gluten_free: bool = True,
                                     max_sugar: Optional[float] = None) -> List[ProteinProduct]:
        """Filter products by dietary preferences."""
        filtered = self.products

        if exclude_beef:
            filtered = [p for p in filtered if not p.contains_beef]

        if exclude_pork:
            filtered = [p for p in filtered if not p.contains_pork]

        if gluten_free:
            filtered = [p for p in filtered if p.is_gluten_free is True]

        if max_sugar is not None:
            filtered = [p for p in filtered if p.sugar_g is not None and p.sugar_g <= max_sugar]

        return filtered


class Recommendation(BaseModel):
    """Model for a product recommendation."""
    rank: int = Field(description="Ranking (1-5)")
    product: ProteinProduct = Field(description="The recommended product")
    rationale: str = Field(description="Why this product is recommended")
    protein_per_dollar: Optional[float] = Field(default=None, description="Protein grams per dollar value")


class ShoppingStrategy(BaseModel):
    """Shopping strategy for visiting stores."""
    store_name: str = Field(description="Store to visit")
    products_to_buy: List[str] = Field(description="List of product names to buy at this store")
    estimated_cost: Optional[float] = Field(default=None, description="Estimated total cost at this store")
    priority: int = Field(description="Visit priority (1=first, 2=second, etc)")


class RecommendationReport(BaseModel):
    """Complete recommendation report."""
    location: str = Field(description="Location for recommendations")
    top_recommendations: List[Recommendation] = Field(description="Top 5 recommended products")
    most_convenient: List[ProteinProduct] = Field(description="Most convenient ready-to-eat options")
    shopping_strategies: List[ShoppingStrategy] = Field(description="Store-by-store shopping strategy")
    total_protein_potential: int = Field(description="Total protein grams from all recommendations")
    estimated_total_budget: Optional[float] = Field(default=None, description="Estimated budget for all recommendations")
    variety_score: str = Field(description="Assessment of protein source variety (e.g., 'Excellent', 'Good', 'Fair')")
    summary: str = Field(description="Overall summary and key takeaways")
