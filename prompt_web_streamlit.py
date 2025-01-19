import os
import streamlit as st
import openai
from openai import OpenAI
from openai import OpenAIError

# Initialize session state for API key
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Set OpenAI API key from environment variable
# Check if the API key exists in session state or environment variable
openai.api_key = st.session_state.get("api_key", os.getenv("OPENAI_API_KEY"))  # Check environment variable as a fallback

# Predefined options for dropdowns and fields
style_options = [
    "",
    "Photorealism", "Surrealism", "Fantasy", "Minimalist", "Abstract", "Dark Fantasy", "Cinematic",
    "Photographic",  "Poster",  "Poster pattern for tapestry", "Painting", "3D Render", "Illustration", "Fashion", "Conceptual Art", "Portrait Photography",
    "Minimalist",
    "Classic",
    "Anime/Manga Style",
    "Pop Art Style",
    "Pencil Sketch Style",
    "Hand-drawn",
    "High contrast",
    "3D-wireframe",
    "Gothic",
    "Fairy tale",
    "Moody with soft tones",
    "Abstract Style",
    "Dynamic",
    "Atmospheric noir",
    "Grainy",
    "Surreal",
    "Ethereal",
    "Luminous with full range of grays",
    "Pixelart"]

medium_styles = [
    {'title': "",'url': "", 'image_url': ""},
    {'title': "Stencil",'url': "", 'image_url': "https://images.ctfassets.net/lzny33ho1g45/20Yk3Cq8WW6EOVPOjorUuO/ce96373bc80fa3763e7e2b301896e14f/ai-art-styles-image10_1.00.28_PM.jpeg?w=1400&fm=avif"},
    {'title': "Watercolor",'url': "", 'image_url': "https://images.ctfassets.net/lzny33ho1g45/4r7n0cynR1HIATzvZ4Hwy6/70254f290f904eb764ed5a0e82d01bbe/ai-art-styles-image35_1.01.26_PM_1.02.08_PM_1.02.54_PM_1.03.20_PM.jpeg?w=1400&fm=avif"},
    {'title': "Papercraft",'url': "", 'image_url': "https://images.ctfassets.net/lzny33ho1g45/twv7V25q9nVCILi6q5krI/9e2f2e8835eff7d21e00c827b65b8403/ai-art-styles-image12.jpeg?w=1400&fm=avif"},
    {'title': "Marker illustration",'url': "", 'image_url': "https://images.ctfassets.net/lzny33ho1g45/7i0ygBRVNnaaTF9DGdDW2S/373c51a364689aa8301f5eb48d4a031d/ai-art-styles-image16_1.01.09_PM.jpeg?w=1400&fm=avif"},
    {'title': "Risograph",'url': "", 'image_url': "https://images.ctfassets.net/lzny33ho1g45/67zpmqSKLXCxAHzktv8J6n/9363d5d44c5d2b39772d23f86e3b8872/ai-art-styles-image2.jpeg?w=1400&fm=avif"},
    {'title': "Graffiti",'url': "", 'image_url': ""},
    {'title': "Ink wash",'url': "", 'image_url': ""},
    {'title': "Quilling",'url': "", 'image_url': ""},
    {'title': "Charcoal",'url': "", 'image_url': ""},
    {'title': "Oil painting",'url': "", 'image_url': ""},
    {'title': "Collage",'url': "", 'image_url': ""},
    {'title': "Mosaic",'url': "", 'image_url': ""},
]

art_styles = [
    {"title": "", "url": "", "image_url": ""},
    {"title": "Abstract Art", "url": "", "image_url": ""},
    {"title": "Academic Art", "url": "", "image_url": ""},
    {"title": "Art Deco", "url": "", "image_url": ""},
    {"title": "CoBrA", "url": "", "image_url": ""},
    {"title": "Color Field Painting", "url": "", "image_url": ""},
    {"title": "Digital Art", "url": "", "image_url": ""},
    {"title": "Fauvism", "url": "", "image_url": ""},
    {"title": "Figurative Art", "url": "", "image_url": ""},
    {"title": "Fine Art", "url": "", "image_url": ""},
    {"title": "Impressionism", "url": "", "image_url": ""},
    {"title": "Minimalism", "url": "", "image_url": ""},
    {"title": "Naïve Art", "url": "", "image_url": ""},
    {"title": "Neo-Impressionism", "url": "", "image_url": ""},
    {"title": "Neon Art", "url": "", "image_url": ""},
    {"title": "Op Art", "url": "", "image_url": ""},
    {"title": "Precisionism", "url": "", "image_url": ""},
    {"title": "Realism", "url": "", "image_url": ""},
    {"title": "Surrealism", "url": "", "image_url": ""},
    {"title": "Symbolism", "url": "", "image_url": ""},
    {"title": "Zero Group", "url": "", "image_url": ""},
    {'title': 'Abstract Expressionism', 'url': 'https://www.studiobinder.com/blog/what-is-abstract-expressionism-definition/', 'image_url': 'httpAbstract Expressionism', 'url': 'https://www.studiobinder.com/blog/what-is-abstract-expressionism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2021/02/What-is-Abstract-Expressionism-Definition-and-History-Featured-1568x882.jpg'},
    {'title': 'Art Nouveau', 'url': 'https://www.studiobinder.com/blog/what-is-art-nouveau-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2021/05/What-is-Art-Nouveau-History-Style-Artists-and-Works-Explained-Featured-1568x882.jpg'},
    {'title': 'Avant-Garde', 'url': 'https://www.studiobinder.com/blog/what-is-avant-garde-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/07/What-is-Avant-Garde-%E2%80%94-Movement-Artists-Works-Explained-Featured-1568x882.jpg'},
    {'title': 'Bauhaus', 'url': 'https://www.studiobinder.com/blog/what-is-bauhaus-art-movement/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/08/What-is-Bauhaus-Art-Movement-Style-History-Explained-Featured-1568x882.jpg'},
    {'title': 'Baroque', 'url': 'https://www.studiobinder.com/blog/what-is-baroque-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/12/What-is-Baroque-Art-Definition-Examples-and-Characteristics-Featured-1568x882.jpg'},
    {'title': 'Classicism', 'url': 'https://www.studiobinder.com/blog/what-is-classicism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2022/11/What-is-Classicism-Art-Definition-Examples-and-History-Featured-1568x882.jpg'},
    {'title': 'Conceptual Art', 'url': 'https://www.studiobinder.com/blog/what-is-conceptual-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2021/02/What-is-Conceptual-Art-Definition-Examples-and-History-Featured-1568x882.jpg'},
    {'title': 'Constructivism Art', 'url': 'https://www.studiobinder.com/blog/what-is-constructivism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2021/02/What-is-Constructivism-Art-Definition-Artists-and-Their-Work-Featured-1568x882.jpg'},
    {'title': 'Contemporary Art', 'url': 'https://www.studiobinder.com/blog/what-is-contemporary-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/04/What-is-Contemporary-Art-Definition-Artists-and-Examples-Featured-1568x882.jpg'},
    {'title': 'Cubism', 'url': 'https://www.studiobinder.com/blog/what-is-cubism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/12/What-is-Cubism-Definition-Examples-and-Iconic-Artists-Featured-1568x882.jpg'},
    {'title': 'Dadaism', 'url': 'https://www.studiobinder.com/blog/what-is-dadaism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/09/What-is-Dadaism-Art-Movement-Style-and-Artists-Explained-Featured-1568x882.jpg'},
    {'title': 'De Stijl', 'url': 'https://www.studiobinder.com/blog/what-is-de-stijl-in-art/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/08/What-is-De-Stijl-in-Art-Movement-Artists-Famous-Works-Featured-1568x882.jpg'},
    {'title': 'Expressionism', 'url': 'https://www.studiobinder.com/blog/what-is-expressionism-art/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/11/What-is-Expressionism-Art-Definition-Examples-and-Artists-Featured-1568x882.jpg'},
    {'title': 'Fluxus', 'url': 'https://www.studiobinder.com/blog/what-is-fluxus-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/04/What-is-Fluxus-%E2%80%94-The-Fluxus-Art-Movement-Works-Explained-Featured-1568x882.jpg'},
    {'title': 'Futurism', 'url': 'https://www.studiobinder.com/blog/what-is-futurism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/03/What-is-Futurism-Art-Movement-Definition-Examples-and-Artists-Featured-1568x882.jpg'},
    {'title': 'Gothic Art', 'url': 'https://www.studiobinder.com/blog/what-is-gothic-art-style/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/08/What-is-Gothic-Art-History-Characteristics-Major-Artists-Featured-1568x882.jpg'},
    {'title': 'Harlem Renaissance', 'url': 'https://www.studiobinder.com/blog/what-was-the-harlem-renaissance-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/07/What-Was-the-Harlem-Renaissance-%E2%80%94-And-Why-It-Mattered-Featured-1568x882.jpg'},
    {'title': 'Installation Art', 'url': 'https://www.studiobinder.com/blog/what-is-installation-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/09/What-is-Installation-Art-Definition-Examples-and-Artists-Featured-1568x882.jpg'},
    {'title': 'Kinetic Art', 'url': 'https://www.studiobinder.com/blog/what-is-kinetic-art/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2022/08/What-is-Kinetic-Art-Movement-Artists-and-History-Explained-Featured-1568x882.jpg'},
    {'title': 'Land Art', 'url': 'https://www.studiobinder.com/blog/what-is-land-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/05/What-is-Land-Art-%E2%80%94-History-of-Earthworks-Land-Art-Movement-Featured-1568x882.jpg'},
    {'title': 'Magical Realism', 'url': 'https://www.studiobinder.com/blog/what-is-magical-realism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/08/What-is-Magical-Realism-Fantasy-vs-Reality-in-Art-and-Literature-Featured-1568x882.jpg'},
    {'title': 'Modern Art', 'url': 'https://www.studiobinder.com/blog/what-is-modern-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/01/What-is-Modern-Art-Definition-History-and-Examples-Featured-1568x882.jpg'},
    {'title': 'Naturalism', 'url': 'https://www.studiobinder.com/blog/what-is-naturalism-in-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/09/What-is-Naturalism-in-Art-History-Style-and-Examples-Featured-1568x882.jpg'},
    {'title': 'Neoclassicism', 'url': 'https://www.studiobinder.com/blog/what-is-neoclassicism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/04/What-is-Neoclassicism-%E2%80%94-Movement-Artists-Art-Explained-Featured-1568x882.jpg'},
    {'title': 'Performance Art', 'url': 'https://www.studiobinder.com/blog/what-is-performance-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/07/What-is-Performance-Art-Definition-Examples-and-History-Featured-1568x882.jpg'},
    {'title': 'Photorealism', 'url': 'https://www.studiobinder.com/blog/what-is-photorealism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/06/What-is-Photorealism-%E2%80%94-The-Art-of-the-Real-Explained-Featured-1568x882.jpg'},
    {'title': 'Pop Art', 'url': 'https://www.studiobinder.com/blog/what-is-pop-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/02/What-is-Pop-Art-Definition-History-Characteristics-and-Artists-Featured-1568x882.jpg'},
    {'title': 'Post-Impressionism', 'url': 'https://www.studiobinder.com/blog/what-is-post-impressionism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/01/What-is-Post-Impressionism-Art-History-Examples-and-Artists-Featured-1568x882.jpg'},
    {'title': 'Primitivism', 'url': 'https://www.studiobinder.com/blog/what-is-primitivism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2022/08/What-is-Primitivism-Movement-Style-Artists-Explained-Featured-1568x882.jpg'},
    {'title': 'Rococo', 'url': 'https://www.studiobinder.com/blog/what-is-rococo-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2021/01/What-is-Rococo-Art-Style-Artists-and-Famous-Works-Explained-Featured-1568x882.jpg'},
    {'title': 'Romanticism', 'url': 'https://www.studiobinder.com/blog/what-is-romanticism-art-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/09/What-is-Romanticism-in-Art-Definition-Examples-and-Traits-Featured-1568x882.jpg'},
    {'title': 'Renaissance', 'url': 'https://www.studiobinder.com/blog/what-was-the-renaissance-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2023/09/What-Was-the-Renaissance-Featured-1568x882.jpg'},
    {'title': 'Street Art', 'url': 'https://www.studiobinder.com/blog/what-is-street-photography-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/04/What-is-Street-Photography-%E2%80%94-Definition-Examples-Styles-Featured-1568x882.jpg'},
    {'title': 'Suprematism', 'url': 'https://www.studiobinder.com/blog/what-is-suprematism-definition/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2020/04/What-is-Suprematism-Art-Movement-Characteristics-Featured-1568x882.jpg'},
    {'title': 'Ukiyo-e', 'url': 'https://www.studiobinder.com/blog/what-is-ukiyo-e-art-paintings/', 'image_url': 'https://s.studiobinder.com/wp-content/uploads/2022/08/What-is-Ukiyo-e-Artists-Characteristics-Best-Examples-Featured-1568x882.jpg'},
]

light_options = [
    {"title": "", "url": "", "image_url": ""},
    {"title": "Soft Glow", "url": "", "image_url": ""},
    {"title": "Golden Hour", "url": "", "image_url": ""},
    {"title": "Moonlight", "url": "", "image_url": ""},
    {"title": "Dynamic Lighting", "url": "", "image_url": ""},
    {"title": "Silhouetted", "url": "", "image_url": ""},
    {"title": "Crisp, soft lighting", "url": "", "image_url": ""},
    {"title": "Warm, golden light", "url": "", "image_url": ""},
    {"title": "Flickering candlelight", "url": "", "image_url": ""},
    {"title": "Interplay of light and shadow", "url": "", "image_url": ""},
    {"title": "Dreamlike glow", "url": "", "image_url": ""},
    {"title": "Silvery moonlight", "url": "", "image_url": ""},
    {"title": "Glowing neon elements", "url": "", "image_url": ""},
    {"title": "Soft bokeh glow", "url": "", "image_url": ""},
    {"title": "Ethereal illumination", "url": "", "image_url": ""},
    {"title": "Partial silhouette / partial illumination", "url": "", "image_url": ""},
    {"title": "golden background", "url": "", "image_url": ""},
    {"title": "Golden aura ", "url": "", "image_url": ""},
    {"title": "dusk lighting", "url": "", "image_url": ""},
    {"title": "Diffused dawn", "url": "", "image_url": ""},
    {"title": "Dawn's Early Light: Gentle, rosy light of breaking dawn", "url": "", "image_url": ""},
    {"title": "Starlight: Twinkling light of a clear night sky", "url": "", "image_url": ""},
    {"title": "Direct Sunlight: Harsh, bright midday light", "url": "", "image_url": ""},
    {"title": "Overcast Light: Soft, diffused light on a cloudy day", "url": "", "image_url": ""},
    {"title": "Lightning: Dramatic flashes during a thunderstorm", "url": "", "image_url": ""},
    {"title": "Artificial Light: Glow of city lights, street lamps, or neon signs", "url": "", "image_url": ""},
    {"title": "Firelight: Warm, flickering light of a campfire or torch", "url": "", "image_url": ""},
    {"title": "Blue Hour: Cool, ethereal light just before sunrise or after sunset", "url": "", "image_url": ""},
    {"title": "Moonlight: Cool, silvery light of the moon", "url": "", "image_url": ""},
    {"title": "Golden Hour: Warm, soft light just after sunrise or before sunset", "url": "", "image_url": ""},
    {"title": "Natural lighting", "url": "", "image_url": ""},
    {"title": "Light and shadow", "url": "", "image_url": ""},
    {"title": "Volumetric lighting", "url": "", "image_url": ""},
    {"title": "Neon lighting", "url": "", "image_url": ""},
    {"title": "Blue hour", "url": "", "image_url": ""},
    {"title": "Backlighting", "url": "", "image_url": ""},
    {"title": "Chiaroscuro", "url": "", "image_url": ""},
    {"title": "God rays", "url": "", "image_url": ""},
    {"title": "Studio lighting", "url": "", "image_url": ""},
    {"title": "Candlelight", "url": "", "image_url": ""},
    {"title": "Street lighting", "url": "", "image_url": ""},
    {"title": "Softbox lighting", "url": "", "image_url": ""},
    {"title": "Moonlight", "url": "", "image_url": ""},
    {"title": "Fairy lights", "url": "", "image_url": ""}
    ]

weather_options = [
    "",
    "Snow: White, hushed serenity",
    " Clear Skies: Endless sky",
    " Windy: Invisible sculptor of grass and water",
    " Rain: Reflective masterpiece",
    " Thunderstorm: Raw energy and electric flashes",
    " Fog: Mysterious veil of shapes and shadows",
    " Sun Shower: Droplets dancing in light",
    " Rainbow: Bridge of colors born from sun and rain",
    " Partly Cloudy: Mix of clear sky and fluffy clouds",
    " Overcast: Blanket of clouds, softening the world in grays",
]

atmosphere_options = [
    "",
    "Mystical", "Whimsical", "Dramatic", "Serene", "Enchanting", "Vibrant",  "Dark and cold ambience",
    "Air of mystery",
    "Enigmatic allure",
    "Chaotic battlefield energy",
    "Tranquil and dreamy",
    "Ethereal and enchanting",
    "Cozy and intimate",
    "Warm and inviting",
    "Stormy and dramatic",
    "Surreal and meditative",
    "Romantic and nostalgic",
    "Futuristic and chaotic"]

camera_types = [
    "",
    "Canon EOS R5",
    "Hassleblad",
    "Nikon D850",
    "Sony Alpha A7 III",
    "Fujifilm X-T4",
    "Leica M10",
    "Hasselblad X1D II 50C",
    "Panasonic Lumix S1R",
    "RED Digital Cinema (RED DSMC2)",
    "ARRI ALEXA Mini",
    "Blackmagic URSA",
    "iPhone 14 Pro",
    "Samsung Galaxy S21 Ultra"
]

camera_angles = [
    {"title": "", "url": "", "image_url": ""},
    {"title": "Low-angle", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/1D9jF1lHuX6KdRXru9EbS6/fd89f2c08bd5a8853f716ebd01b74266/ai-art-styles-image31_1.01.24_PM_1.02.05_PM_1.02.51_PM.jpeg?w=1400&fm=avif"},
    {"title": "High-angle", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/3hCCEUgvbJhCeTkI9PCbBY/a0e72b5a4799566d7660e107e0fba8f2/ai-art-styles-image11.jpeg?w=1400&fm=avif"},
    {"title": "Mid-angle", "url": "", "image_url": ""},
    {"title": "Eye-level", "url": "", "image_url": ""},
    {"title": "Close-up", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/1m23oYFXlZCPVlxFQXlTbT/0ed276e326abea3d66c0d4056052e18f/ai-art-styles-image38_1.01.28_PM_1.02.09_PM_1.02.55_PM_1.03.22_PM.jpeg?w=1400&fm=avif"},
    {"title": "Bokeh", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/3kHrWfFKLVVVnEkRsHKdtz/11d287ecbdd9986bc20052559fec8fac/ai-art-styles-image29_1.01.23_PM_1.02.04_PM_1.02.50_PM.jpeg?w=1400&fm=avif"},
    {"title": "Dutch angle", "url": "", "image_url": ""},
    {"title": "Over-the-shoulder", "url": "", "image_url": ""},
    {"title": "Overhead Shot", "url": "", "image_url": ""},
    {"title": "Other-the-shoulder shot / short over", "url": "", "image_url": ""},
    {"title": "Low shutter speed", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/5ntuVvj6h3XTotv1eZrDFj/13706d369ae01ac87a6d58f0acb35559/ai-art-styles-image5.jpeg?w=1400&fm=avif"},
    {"title": "Bird’s-eye view / Aerial angle", "url": "", "image_url": ""},
    {"title": "Worm’s-eye view", "url": "", "image_url": ""},
    {"title": "Macro shot", "url": "", "image_url": "https://cdn.prod.website-files.com/62233c592d2a1e009d42f46c/66d2ab901613305712037855_6601fd33248b6691c47299a9_intelligence%2520artificielle%252015.webp"},
    {"title": "Extreme Close-Up", "url": "", "image_url": ""},
    {"title": "Fish-eye", "url": "", "image_url": "https://cdn.prod.website-files.com/62233c592d2a1e009d42f46c/66d2ab90161330571203784c_6601fd4255aba152391af2c4_intelligence%2520artificielle%252017.webp"},
    {"title": "Wide-angle shot", "url": "", "image_url": ""},
    {"title": "Panoramic View", "url": "", "image_url": ""},
    {"title": "Point-of-view (POV)", "url": "", "image_url": ""},
    {"title": "Framed View", "url": "", "image_url": ""},
    {"title": "Reflection View", "url": "", "image_url": ""},
    {"title": "High Angle: Comprehensive overview from above", "url": "", "image_url": ""},
    {"title": "Rule of Thirds: Positioning subject along grid lines/intersections", "url": "", "image_url": ""},
    {"title": "Low Angle: Emphasizing foreground and depth", "url": "", "image_url": ""},
    {"title": "Framing: Using elements to focus on the subject", "url": "", "image_url": ""},
    {"title": "Diagonal: Establishing movement through composition", "url": "", "image_url": ""},
    {"title": "Symmetry: Creating balance and harmony", "url": "", "image_url": ""},
    {"title": "Worm's Eye View: Looking up from ground level", "url": "", "image_url": ""},
    {"title": "Juxtaposition: Contrasting elements for visual interest", "url": "", "image_url": ""},
    {"title": "Bird's Eye View: Soaring above the scene", "url": "", "image_url": ""},
    {"title": "Leading Lines: Natural or architectural lines guiding the eye", "url": "", "image_url": ""}
]

camera_positions = ["",
    "Frontal shot",
    "3/4 front angle",
    "Profile (left side)",
    "Profile (right side)",
    "Behind the subject",
    "Over-the-shoulder",
    "Overhead / top-down",
    "Eye-level directly in front",
    "Low position looking up",
    "High position looking down",
    "Drone view",
    "Aerial view",
    "Satellite view",
]

color_palettes = [
    {"title": "", "url": "", "image_url": ""},
    {"title": "Cool tones", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/gjQkLB02nJ48QZ1H7hPjO/ab51d59239cb43f5708f990a7029e710/ai-art-styles-image32_1.01.25_PM_1.02.06_PM_1.02.52_PM.jpeg?w=1400&fm=avif"},
    {"title": "Warm tones", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/84zfHtI8W08eOH2pt2TY0/d292170c0f366b300615a56cea12791c/ai-art-styles-image19_1.01.17_PM.jpeg?w=1400&fm=avif"},
    {"title": "Vibrant", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/26oGdmmBbHsGJwY8r8Kiyw/03831104f21c63de10a29c8791a0001e/ai-art-styles-image17_1.01.09_PM.jpeg?w=1400&fm=avif"},
    {"title": "Pastels", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/4BInn02gkFdVs8iPoYvn9k/88e51812094714d6acc541c6465edfbc/ai-art-styles-image18_1.01.17_PM.jpeg?w=1400&fm=avif"},
    {"title": "Earth tones", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/4NjaBp117XJHQCJmttLDQ1/4e1a63650ad367ef7cefb42fd9dd638a/ai-art-styles-image23_1.01.20_PM_1.01.58_PM.jpeg?w=1400&fm=avif"},
    {"title": "Jewel tones", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/5pNrEqd8PamNwfoGFySuuN/4edf3a581b7101e16c2e6e5f842f723a/ai-art-styles-image13.jpeg?w=1400&fm=avif"},
    {"title": "Saffron yellow", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/5E3ec5P3sFJE5HaPXuw4hy/30ec9eae5b610846443e7ca4118b58d2/ai-art-styles-image24_1.01.20_PM_1.01.58_PM.jpeg?w=1400&fm=avif"},
    {"title": "Forest green", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/2aa3Use90tPFrfl9VDsbYx/a2d2f705ecd5f273dc5a2b9f912f3f2b/ai-art-styles-image25_1.01.21_PM_1.01.59_PM.jpeg?w=1400&fm=avif"},
    {"title": "peacock blue and saffron yellow", "url": "", "image_url": "https://images.ctfassets.net/lzny33ho1g45/6sdx0r3kHTm0rsTj43cbfo/83576b8120c4b9fc2241d8c8b2f9fdad/ai-art-styles-image34_1.01.26_PM_1.02.07_PM_1.02.53_PM_1.03.19_PM.jpeg?w=1400&fm=avif"},
    {"title": "Monochromatic blues", "url": "", "image_url": ""},
    {"title": "Earthy reds and oranges", "url": "", "image_url": ""},
    {"title": "Neon graffiti", "url": "", "image_url": ""},
    {"title": "Autumn leaves", "url": "", "image_url": ""},
    {"title": "Deep sea blues", "url": "", "image_url": ""},
    {"title": "Grayscale", "url": "", "image_url": ""},
    {"title": "Sepia", "url": "", "image_url": ""},
    {"title": "Primary colors", "url": "", "image_url": ""},
    {"title": "Rainbow spectrum", "url": "", "image_url": ""},
    {"title": "Metallics", "url": "", "image_url": ""},
    {"title": "Pure Black and white", "url": "", "image_url": ""},
    {"title": "Monochrome (black, white, and shades of gray)", "url": "", "image_url": ""},
    {"title": "Warm earthy tones (browns, ochres, deep oranges)", "url": "", "image_url": ""},
    {"title": "Vibrant neon colors (electric pinks, greens, blues)", "url": "", "image_url": ""},
    {"title": "Soft pastel hues (pale pink, mint, lavender, baby blue)", "url": "", "image_url": ""},
    {"title": "Retro sepia filter (browns, faded yellows, vintage feel)", "url": "", "image_url": ""},
    {"title": "Bold primary colors (red, yellow, blue)", "url": "", "image_url": ""},
    {"title": "Dark moody blues and purples", "url": "", "image_url": ""},
    {"title": "Metallic gold and silver accents", "url": "", "image_url": ""},
    {"title": "High contrast black and white", "url": "", "image_url": ""},
    {"title": "Muted colours", "url": "", "image_url": ""},
    {"title": "Muted neutral shades (taupe, beige, dusty gray)", "url": "", "image_url": ""},
    {"title": "Nature Tropicale: Vert Émeraude (#2ECC71), Bleu Océan (#3498DB), Jaune Soleil (#F1C40F), Orange Mangue (#E67E22), Rouge Hibiscus (#E74C3C)", "url": "", "image_url": ""},
    {"title": "Luxe et Élégance: Noir Profond (#1C1C1C), Or Riche (#FFD700), Blanc Ivoire (#FFFFF0), Bordeaux Velours (#800020), Gris Argenté (#C0C0C0)", "url": "", "image_url": ""},
    {"title": "Rêve Pastel: Rose Poudré (#FADADD), Bleu Lavande (#B0E0E6), Jaune Vanille (#FFFACD), Vert Menthe (#98FF98), Gris Clair (#D3D3D3)", "url": "", "image_url": ""},
    {"title": "Terre et Nature: Vert Forêt (#228B22), Marron Terre (#8B4513), Beige Sable (#F5DEB3), Bleu Ciel (#87CEEB), Jaune Moutarde (#D2B48C)", "url": "", "image_url": ""},
    {"title": "Futuriste Néon: Rose Fluo (#FF007F), Bleu Cyan (#00FFFF), Vert Néon (#39FF14), Violet Laser (#8A2BE2), Noir Nuit (#000000)", "url": "", "image_url": ""},
    {"title": "Vintage Rétro: Rouge Brique (#B22222), Jaune Doré (#DAA520), Vert Olive (#808000), Bleu Pétrole (#4682B4), Beige Vieilli (#DEB887)", "url": "", "image_url": ""},
    {"title": "Hiver Mystique: Bleu Glacial (#ADD8E6), Blanc Neige (#FFFFFF), Gris Ardoise (#708090), Bleu Nuit (#191970), Argent Givré (#DCDCDC)", "url": "", "image_url": ""},
    {"title": "Soleil Coucher: Orange Brûlé (#FF4500), Rose Saumon (#FFA07A), Rouge Sang (#DC143C), Jaune Safran (#FFD700), Violet Crépuscule (#8B008B)", "url": "", "image_url": ""},
    {"title": "Minimaliste Monochrome: Noir Charbon (#2B2B2B), Gris Anthracite (#555555), Gris Clair (#D4D4D4), Blanc Pur (#FFFFFF)", "url": "", "image_url": ""},
    {"title": "Fantaisie Féérique: Rose Magenta (#FF00FF), Bleu Royal (#4169E1), Jaune Lumière (#FFFF33), Vert Émeraude Lumineux (#00FF7F), Violet Mystique (#8A2BE2)", "url": "", "image_url": ""},
    {"title": "Rainbow gradient (prismatic, multi-colored blend)", "url": "", "image_url": ""},
]

print("\n--------------------------------------------------")
print("NEW SESSION")
print("--------------------------------------------------")

# Modern minimalist style for the UI
st.set_page_config(page_title="AI Picture Prompt Generator", layout="centered", initial_sidebar_state="collapsed")

# Verify API key is set (for debugging)
# if not openai.api_key:
#     st.error("OpenAI API Key is missing. Please set it by the Generate AI prompt button")

# -----------------------------------------------------
# Statement management
# -----------------------------------------------------
# Initialize session state for the generated prompt
if "generated_prompt" not in st.session_state:
    print("Empty -> st.session_state.generated_prompt")
    st.session_state.generated_prompt = ""
else:
    generated_prompt = st.session_state.generated_prompt
    print(f"st.session_state.generated_prompt = {generated_prompt}")

# -----------------------------------------------------
# Object to update
# -----------------------------------------------------

# -----------------------------------------------------
# UI Functions
# -----------------------------------------------------
def create_art_display(parameter_art):
            
    # Filter out items with empty or missing image_url
    filtered_art = [art for art in parameter_art if art.get("image_url")]

    # Now make rows of three columns from the filtered list
    for i in range(0, len(filtered_art), 3):
        row_items = filtered_art[i:i+3]
        # Create as many columns as there are items in this row
        cols = st.columns(len(row_items))
        for col, art in zip(cols, row_items):
            title = art.get("title", "")
            image_url = art.get("image_url", "")
            with col:
                st.image(image_url, width=130, caption=title)

def display_parameter_dropbox(parameter_text, parameter_pictures):
    # Create two columns with different widths
    col1, col2 = st.columns([2, 1])  # col1 is twice as wide as col2

    # Add widgets to the columns
    with col1:
        all_titles = [item["title"] for item in parameter_pictures]
        result = st.selectbox(parameter_text, options = all_titles, index = 0)

    with col2:
        st.write("")
        st.write("")
        with st.popover(parameter_text):
            # Render the art styles inside the popup
            create_art_display(parameter_pictures)

    return result

# Inject dynamic CSS to override Streamlit styles
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            color: #333;
        }
        .stApp {
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stTextInput > div > input, .stTextArea textarea {
            background-color: #f3f4f6 !important;
            color: #333 !important;                 /* Dark text */
            border-radius: 8px !important;
            border: 1px solid #ddd !important;
            padding: 0.5rem !important;
            font-size: 1rem !important;
        }
        .stSelectbox > div {
            background-color: #f3f4f6 !important;
            border-radius: 8px !important;
        }
        .stButton > button {
            background-color: #007BFF;
            color: white;
            border-radius: 8px;
            border: none;
            font-size: 1rem;
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .stButton > button[disabled] {
            background-color: #cccccc !important;
            color: #666666 !important;
            border: 0px solid #999999 !important;
            border-radius: 8px;
            font-size: 1rem;
            padding: 0.5rem 1rem;
            cursor: not-allowed !important;
        }
        .stRadio div {
            flex-direction: row !important;
            gap: 1rem;
        }
        .stRadio div label {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.9rem;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title("AI Picture Prompt Generator")
st.write("Create a detailed picture prompt by filling in the fields below. Let the AI craft the perfect description for your visual idea!")
# st.write(f"API Key: {openai.api_key}")

# User Inputs
# st.header("Prompt Details")
topic = st.text_input("The focus and position (e.g., A lion conducting an orchestra):", "invent a prompt that is fun and creative")
ratio = st.radio(
    "Aspect Ratio:",
    options = ["Landscape", "Square", "Portrait"],
    index = 0,
    format_func = lambda x: x.capitalize(),
)
composition = st.text_area("Composition (e.g., the lion is on the left hand side):", "")
background = st.text_area("Background Elements (e.g., moonlit forest clearing):", "")

style = st.selectbox("Picture Style:", options = style_options, index = 0)
art_style = display_parameter_dropbox("Art style", art_styles)
medium_style = display_parameter_dropbox("Medium:", medium_styles)
light = display_parameter_dropbox("Lighting Style:",light_options)
weather = st.selectbox("Weather:", options =  weather_options  , index = 0)
atmosphere = st.selectbox("Atmosphere:", options = atmosphere_options, index = 0)
camera_type = st.selectbox("Camera type:", options = camera_types, index = 0)
camera_angle = display_parameter_dropbox("Camera angle:", camera_angles)
camera_position = st.selectbox("Camera position:", options = camera_positions, index = 0)
color_palette = display_parameter_dropbox("Color palette:", color_palettes)

st.markdown("[You can find more style here](https://freeflo.ai/styles/)")
additional_style = st.text_area("Add your own style (e.g. Ethereal Painting, Funk Art, etc.):", "")

# Creativity Slider
temperature = st.slider(
    "Creativity Level (Temperature):",
    min_value=0.1,
    max_value=0.9,
    value=0.7,
    step=0.1,
    help="Adjust the creativity level. Lower values make the output more deterministic, while higher values add randomness."
)

# -------------------------------------------------------
# Generate BASIC Prompt Button
# -------------------------------------------------------
if st.button("Generate Basic Prompt"):
 
    print(f"Basic Button pressed -> generated_prompt = {generated_prompt}")

    prompt_parts = ["Create a picture using the following instructions:"]
    if topic: prompt_parts.append(f"* Primary focus element: {topic}")
    if composition: prompt_parts.append(f"* Composition: {composition}")
    if background: prompt_parts.append(f"* Background: {background}")
    if style: prompt_parts.append(f"* Style: {style}")
    if medium_style: prompt_parts.append(f"* Medium type: {medium_style}")
    if style: prompt_parts.append(f"* Art Style: {style}")
    if light: prompt_parts.append(f"* Lighting: {light}")
    if weather: prompt_parts.append(f"* Weather: {weather}")
    if atmosphere: prompt_parts.append(f"* Atmosphere: {atmosphere}")
    if camera_type: prompt_parts.append(f"* Camera type: {camera_type}")
    if camera_angle: prompt_parts.append(f"* Camera angle: {camera_angle}")
    if camera_position: prompt_parts.append(f"* Camera position: {camera_position}")
    if color_palette: prompt_parts.append(f"* Color palette: {color_palette}")
    if additional_style: prompt_parts.append(f"* Additional picture style: {additional_style}")
    if ratio: prompt_parts.append(f"* Aspect Ratio: {ratio}")

    prompt_structure = "\n".join(prompt_parts)
    # Store the generated prompt in session state
    st.session_state.generated_prompt = prompt_structure

    # Update the Markdown placeholder with the latest generated prompt
    if st.session_state.generated_prompt:
        print("3/ After Basic button pressed -> update Markdown")
    else:
        print("3/ After Basic button pressed -> st.session_state.generated_prompt EMPTY")

 
# -------------------------------------------------------
# Generate AI complext Prompt Button
# -------------------------------------------------------
# Add a single-line text field for the API key
# Display appropriate input or message
if st.session_state.api_key:
    st.success("API Key is already set.")
    st.write("Your API Key is stored securely and ready to use.")
    print(f"API Key = {openai.api_key}")
else:
    # Allow the user to input the API key if not set
    api_key_input = st.text_input(
        "Enter your API Key:",
        placeholder="Your API Key here",
        type="password"
    )

    # Save API key on submission
    if st.button("Save API Key"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            openai.api_key = api_key_input
            print(f"API Key = {openai.api_key}")
            st.success("API Key has been saved!")
        else:
            st.error("Please enter a valid API Key.")

# Disable the "Generate AI Prompt" button if the API Key is not set
is_api_key_set = st.session_state.api_key is not None

if st.button("Generate AI Prompt (Open AI)", disabled=not is_api_key_set):
    # Combine user inputs into a structured prompt
    prompt_structure = (
        f"### Primary focus element:\n{topic}\n"
        f"### Composition:\n{composition}\n"
        f"### Background:\n{background}\n"
        f"### Style:\n{style}\n"
        f"### Art Style:\n{style}\n"
        f"### Lighting:\n{light}\n"
        f"### Weather:\n{weather}\n"
        f"### Atmosphere:\n{atmosphere}\n"
        f"### Camera type:\n{camera_type}\n"
        f"### Camera angle:\n{camera_angle}\n"
        f"### Camera position:\n{camera_position}\n"
        f"### Color palette:\n{color_palette}\n"
        f"### Aspect Ratio:\n{ratio}\n"
    )

    # Call the OpenAI API to generate the description
    print(f"API Key = {openai.api_key}")
    # st.write(f"API Key: {openai.api_key}")

    # Set API in header
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant for generating creative prompts."
            },
            {
                "role": "user",
                "content": f"Create a detailed and structured visual prompt for generating an image based on the following inputs:\n{prompt_structure}"
            }
        ],
        "max_tokens": 600,
        "temperature": temperature
    }
    try:
        # random_text = random.randint(1, 100)
        # time.sleep(1)
        # generated_prompt = f"### {random_text}\n\n{prompt_structure}"

        client = OpenAI(api_key=openai.api_key)

        print(f"AI Button pressed -> generated_prompt = {generated_prompt}")

        # Call OpenAI API using the Python SDK
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for generating creative prompts."
                },
                {
                    "role": "user",
                    "content": f"Create a detailed and structured visual prompt for generating an image based on the following inputs:\n{prompt_structure}"
                }
            ],
            max_tokens=600,
            temperature=temperature,
        )

        # Extract the generated content
        generated_prompt = response.choices[0].message.content
        token_usage = response.usage.total_tokens

        # Log the result
        print(f'OK token used = {token_usage} -> result {generated_prompt}')
        st.session_state.generated_prompt = generated_prompt

    except OpenAIError as e:
        # Handle errors gracefully
        st.error(f"An error occurred while generating the prompt: {e}")
        print(f"OpenAI API error: {e}")
        generated_prompt = ""

    except Exception as e:
        # Handle other exceptions
        st.error(f"An unexpected error occurred: {e}")
        print(f"Unexpected error: {e}")

    #     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #     if response.status_code == 200:
    #         try:
    #             token = response.json()['usage']['total_tokens']
    #             generated_prompt = response.json()['choices'][0]['message']['content']
    #             print(f'OK token used = {token} -> result {generated_prompt}')
    #         except (KeyError, IndexError) as e:
    #             print(f"/!\ Error extracting content from response: {e}")
    #             generated_prompt = ""
    #             st.error(f"Error: {e}")
    #     else:
    #         print(f"/!\ OpenAI API error: {response.text}")
    #         st.error(f"Error code = {response.status_code} -> {response.text}")
    #         generated_prompt = ""

    #     # Store the generated prompt in session state
    #     st.session_state.generated_prompt = generated_prompt

    #     # Update the Markdown placeholder with the latest generated prompt
    #     if st.session_state.generated_prompt:
    #         print("3/ After AI button pressed -> update Markdown")
    #     else:
    #         print("3/ After AI button pressed -> st.session_state.generated_prompt EMPTY")

    # except Exception as e:
    #     st.error(f"An error occurred while generating the prompt: {e}")

# # Display the generated prompt if it exists
# if "generated_prompt" in st.session_state and st.session_state.generated_prompt:
#     generated_prompt = st.session_state.generated_prompt

# else:
#     print("1/ st.session_state.generated_prompt EMPTY")
#     st.write("No prompt was generated. Please try again.")

# Update the Markdown placeholder with the latest generated prompt
if st.session_state.generated_prompt:
    # Display the generated prompt
    st.subheader("Generated Prompt")
    print("2/ st.session_state.generated_prompt EXIST")
    st.code(st.session_state.generated_prompt, language="markdown")
    #  st.write(st.session_state.generated_prompt, unsafe_allow_html=True)
else:
    print("2/ st.session_state.generated_prompt EMPTY !")
