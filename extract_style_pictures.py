from bs4 import BeautifulSoup
import requests

# List of art style URLs
art_styles = [
    {"title": "Abstract Expressionism", "url": "https://www.studiobinder.com/blog/what-is-abstract-expressionism-definition/"},
    {"title": "Art Nouveau", "url": "https://www.studiobinder.com/blog/what-is-art-nouveau-definition/"},
    {"title": "Avant-Garde", "url": "https://www.studiobinder.com/blog/what-is-avant-garde-definition/"},
    {"title": "Bauhaus", "url": "https://www.studiobinder.com/blog/what-is-bauhaus-art-movement/"},
    {"title": "Baroque", "url": "https://www.studiobinder.com/blog/what-is-baroque-definition/"},
    {"title": "Classicism", "url": "https://www.studiobinder.com/blog/what-is-classicism-art-definition/"},
    {"title": "Conceptual Art", "url": "https://www.studiobinder.com/blog/what-is-conceptual-art-definition/"},
    {"title": "Constructivism Art", "url": "https://www.studiobinder.com/blog/what-is-constructivism-art-definition/"},
    {"title": "Contemporary Art", "url": "https://www.studiobinder.com/blog/what-is-contemporary-art-definition/"},
    {"title": "Cubism", "url": "https://www.studiobinder.com/blog/what-is-cubism-definition/"},
    {"title": "Dadaism", "url": "https://www.studiobinder.com/blog/what-is-dadaism-art-definition/"},
    {"title": "De Stijl", "url": "https://www.studiobinder.com/blog/what-is-de-stijl-in-art/"},
    {"title": "Expressionism", "url": "https://www.studiobinder.com/blog/what-is-expressionism-art/"},
    {"title": "Fluxus", "url": "https://www.studiobinder.com/blog/what-is-fluxus-art-definition/"},
    {"title": "Futurism", "url": "https://www.studiobinder.com/blog/what-is-futurism-definition/"},
    {"title": "Gothic Art", "url": "https://www.studiobinder.com/blog/what-is-gothic-art-style/"},
    {"title": "Harlem Renaissance", "url": "https://www.studiobinder.com/blog/what-was-the-harlem-renaissance-definition/"},
    {"title": "Installation Art", "url": "https://www.studiobinder.com/blog/what-is-installation-art-definition/"},
    {"title": "Kinetic Art", "url": "https://www.studiobinder.com/blog/what-is-kinetic-art/"},
    {"title": "Land Art", "url": "https://www.studiobinder.com/blog/what-is-land-art-definition/"},
    {"title": "Magical Realism", "url": "https://www.studiobinder.com/blog/what-is-magical-realism-definition/"},
    {"title": "Modern Art", "url": "https://www.studiobinder.com/blog/what-is-modern-art-definition/"},
    {"title": "Naturalism", "url": "https://www.studiobinder.com/blog/what-is-naturalism-in-art-definition/"},
    {"title": "Neoclassicism", "url": "https://www.studiobinder.com/blog/what-is-neoclassicism-art-definition/"},
    {"title": "Performance Art", "url": "https://www.studiobinder.com/blog/what-is-performance-art-definition/"},
    {"title": "Photorealism", "url": "https://www.studiobinder.com/blog/what-is-photorealism-definition/"},
    {"title": "Pop Art", "url": "https://www.studiobinder.com/blog/what-is-pop-art-definition/"},
    {"title": "Post-Impressionism", "url": "https://www.studiobinder.com/blog/what-is-post-impressionism-art-definition/"},
    {"title": "Primitivism", "url": "https://www.studiobinder.com/blog/what-is-primitivism-art-definition/"},
    {"title": "Rococo", "url": "https://www.studiobinder.com/blog/what-is-rococo-art-definition/"},
    {"title": "Romanticism", "url": "https://www.studiobinder.com/blog/what-is-romanticism-art-definition/"},
    {"title": "Renaissance", "url": "https://www.studiobinder.com/blog/what-was-the-renaissance-definition/"},
    {"title": "Street Art", "url": "https://www.studiobinder.com/blog/what-is-street-photography-definition/"},
    {"title": "Suprematism", "url": "https://www.studiobinder.com/blog/what-is-suprematism-definition/"},
    {"title": "Ukiyo-e", "url": "https://www.studiobinder.com/blog/what-is-ukiyo-e-art-paintings/"}
]

# Function to fetch the top image URL from a given webpage
def fetch_top_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the first image with the required format
        image_tag = soup.find('img', {'src': lambda x: x and x.startswith('https://s.studiobinder.com/wp-content/uploads/')})
        if image_tag:
            return image_tag['src']
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        return None

# Create a new list with the image URLs
for style in art_styles:
    print(f"- STYLE = {style['url']}")
    style['image_url'] = fetch_top_image(style['url'])

# Print the results
print("\n\n")

# Print the results as a Python list
result_list = [
    {
        "title": style['title'],
        "url": style['url'],
        "image_url": style.get('image_url')
    }
    for style in art_styles
]

# Print each dictionary on a new line
for style in result_list:
    print(f"{style},")

# for style in art_styles:
#     print(f"Title: {style['title']}, URL:{style['url']}, Image URL: {style.get('image_url')}")