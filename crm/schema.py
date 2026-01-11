"""
GraphQL schema for CRM application.
"""
import graphene
from graphene_django import DjangoObjectType
from .models import Product


class ProductType(DjangoObjectType):
    """GraphQL type for Product model."""
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock', 'price')


class UpdateLowStockProducts(graphene.Mutation):
    """Mutation to update low-stock products (stock < 10) by incrementing stock by 10."""
    class Arguments:
        pass  # No arguments needed
    
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)
    
    def mutate(self, info):
        """Execute the mutation to update low-stock products."""
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        updated_products = []
        for product in low_stock_products:
            # Increment stock by 10 (simulating restocking)
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        return UpdateLowStockProducts(
            success=True,
            message=f"Successfully updated {len(updated_products)} product(s)",
            updated_products=updated_products
        )


class Query(graphene.ObjectType):
    """GraphQL queries."""
    hello = graphene.String(default_value="Hello, GraphQL!")
    products = graphene.List(ProductType)
    
    def resolve_products(self, info):
        """Resolve all products."""
        return Product.objects.all()


class Mutation(graphene.ObjectType):
    """GraphQL mutations."""
    update_low_stock_products = UpdateLowStockProducts.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

