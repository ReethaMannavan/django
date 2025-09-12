from rest_framework import serializers
from .models import Restaurant, Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'available', 'category', 'restaurant']



class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(source='menuitem_set', many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'menu_items']
