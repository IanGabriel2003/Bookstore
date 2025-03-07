import pytest
from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer
from order.serializers.order_serializer import OrderSerializer

@pytest.mark.django_db
def test_category_serializer():
    """ Testa a serialização de uma categoria """
    category = Category.objects.create(
        title="Eletrônicos",
        slug="eletronicos",
        description="Categoria de eletrônicos",
        active=True
    )

    serializer = CategorySerializer(category)
    expected_data = {
        "title": "Eletrônicos",
        "slug": "eletronicos",
        "description": "Categoria de eletrônicos",
        "active": True,
    }

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_product_serializer():
    """ Testa a serialização de um produto com categoria """
    category = Category.objects.create(
        title="Celulares",
        slug="celulares",
        description="Categoria de celulares",
        active=True
    )

    product = Product.objects.create(
        title="iPhone 15",
        description="Novo iPhone com tela OLED",
        price=7999.99,
        active=True
    )

    product.category.add(category)  # Adicionando a categoria ao produto
    serializer = ProductSerializer(product)

    assert serializer.data["title"] == "iPhone 15"
    assert serializer.data["description"] == "Novo iPhone com tela OLED"
    assert serializer.data["price"] == 7999.99
    assert serializer.data["active"] is True
    assert serializer.data["category"][0]["title"] == "Celulares"  # Verifica se a categoria foi associada corretamente


@pytest.mark.django_db
def test_order_serializer():
    """ Testa a serialização de um pedido com produtos """
    category = Category.objects.create(
        title="Informática",
        slug="informatica",
        description="Categoria de informática",
        active=True
    )

    product1 = Product.objects.create(
        title="Mouse Gamer",
        description="Mouse com RGB e 16000 DPI",
        price=299.99,
        active=True
    )

    product2 = Product.objects.create(
        title="Teclado Mecânico",
        description="Teclado com switches Cherry MX",
        price=599.99,
        active=True
    )

    product1.category.add(category)
    product2.category.add(category)

    order_data = {"product": [product1, product2]}  # Criando um dicionário para testar a serialização
    serializer = OrderSerializer(data=order_data)

    assert serializer.is_valid(), serializer.errors  # Verifica se a serialização foi bem-sucedida
    assert serializer.validated_data["product"] == [product1, product2]  # Confirma que os produtos foram serializados corretamente
