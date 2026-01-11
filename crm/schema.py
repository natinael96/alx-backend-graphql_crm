"""
GraphQL schema for CRM application.
"""
import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order


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


class CustomerType(DjangoObjectType):
    """GraphQL type for Customer model."""
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'created_at')


class OrderType(DjangoObjectType):
    """GraphQL type for Order model."""
    class Meta:
        model = Order
        fields = ('id', 'customer', 'total_amount', 'created_at')


class Query(graphene.ObjectType):
    """GraphQL queries."""
    hello = graphene.String(default_value="Hello, GraphQL!")
    products = graphene.List(ProductType)
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Decimal()
    
    def resolve_products(self, info):
        """Resolve all products."""
        return Product.objects.all()
    
    def resolve_customers(self, info):
        """Resolve all customers."""
        return Customer.objects.all()
    
    def resolve_orders(self, info):
        """Resolve all orders."""
        return Order.objects.all()
    
    def resolve_total_customers(self, info):
        """Resolve total number of customers."""
        return Customer.objects.count()
    
    def resolve_total_orders(self, info):
        """Resolve total number of orders."""
        return Order.objects.count()
    
    def resolve_total_revenue(self, info):
        """Resolve total revenue (sum of total_amount from orders)."""
        from django.db.models import Sum
        result = Order.objects.aggregate(total=Sum('total_amount'))
        return result['total'] or 0


class Mutation(graphene.ObjectType):
    """GraphQL mutations."""
    update_low_stock_products = UpdateLowStockProducts.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

