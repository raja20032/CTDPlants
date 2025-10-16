import json
import os

# First, let's create the plant data JSON file
plants_data = {
    "plants": [
    {
      "id": 1,
      "name": "Sunflower",
      "description": "Bright, cheerful flowers that follow the sun",
      "price": 33.50,
      "size": "big",
      "color": "yellow",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXaUGstQ0Of_2J82X7oFr5vQP_3J9SGcgEyA&s"
    },
    {
      "id": 2,
      "name": "Rose Bush",
      "description": "Classic red roses perfect for any garden",
      "price": 24.90,
      "size": "medium",
      "color": "red",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQe-FnTx7NYDJsl11OWAR5yG2qmb96hq2ZcBg&s"
    },
    {
      "id": 3,
      "name": "Lavender",
      "description": "Fragrant purple flowers with calming properties",
      "price": 18.50,
      "size": "medium",
      "color": "purple",
      "image": "https://hedgexpress.co.uk/wp-content/uploads/2024/12/DB8A3843-300x300.jpeg"
    },
    {
      "id": 4,
      "name": "Marigold",
      "description": "Vibrant orange flowers that bloom all season",
      "price": 8.50,
      "size": "small",
      "color": "orange",
      "image": "https://www.chengtainursery.com/wp-content/uploads/2024/09/photo_1_2024-09-26_12-01-01-Photoroom-300x300.png"
    },
    {
      "id": 5,
      "name": "Daisy",
      "description": "Simple, elegant white flowers with a floral-woody fragrance",
      "price": 10.00,
      "size": "small",
      "color": "white",
      "image": "https://i.pinimg.com/474x/88/f8/2b/88f82bcf680466f311fc0d6937041ec0.jpg"
    },
    {
      "id": 6,
      "name": "Hydrangea",
      "description": "Large clusters of beautiful blue flowers",
      "price": 32.50,
      "size": "big",
      "color": "blue",
      "image": "https://www.gardenia.net/wp-content/uploads/2023/05/hydrangea-macrophylla-blue-heaven-300x300.webp"
    },
    {
      "id": 7,
      "name": "Tulips",
      "description": "Delicate spring flowers in soft pink",
      "price": 15.99,
      "size": "medium",
      "color": "pink",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbEqQL7M0c1hy-W2Pom5pNXRGShxQYFfQc9w&s"
    },
    {
      "id": 8,
      "name": "Basil Plant",
      "description": "Fresh herbs for cooking, easy to grow",
      "price": 6.90,
      "size": "small",
      "color": "green",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3oXy3A4Y3bRP3RWZysdTRdYer9S9-iVKuxQ&s"
    },
    {
      "id": 9,
      "name": "Birch Sapling",
      "description": "Smooth, resinous, varicoloured or white bark",
      "price": 35.50,
      "size": "big",
      "color": "green",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_xKhNFfq8vOA6Hov6ko2DBRTsbJyeACbUaA&s"
    },
    {
      "id": 10,
      "name": "Petunias",
      "description": "Colorful cascading flowers perfect for containers",
      "price": 10,
      "size": "small",
      "color": "purple",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZ4TxDEK0kSc0GT0FEPhDo_vJYOhIZFu5lHA&s"
    },
    {
      "id": 11,
      "name": "Geranium",
      "description": "Classic red flowers that bloom continuously",
      "price": 15.50,
      "size": "medium",
      "color": "red",
      "image": "https://finelineslandscaping.co.za/images/shop/pelargonium-zonale-kariba-red-300x300.webp"
    },
    {
      "id": 12,
      "name": "Oak Sapling",
      "description": "A mighty oak that will grow for generations",
      "price": 45.00,
      "size": "big",
      "color": "green",
      "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0itT_rLt-bIyWl_zg0-aOzmKZ2tHo0PiK6Q&s"
    }
  ]
}

# Save the plants data
with open('plants_data.json', 'w') as f:
    json.dump(plants_data, f, indent=2)

print("Created plants_data.json with", len(plants_data['plants']), "plants")