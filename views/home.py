import streamlit as st

# Custom CSS to improve aesthetics
st.markdown("""
    <style>
        .block-container {padding-top: 2rem !important;}
        .main-title {text-align: center; font-size: 7rem !important; font-weight: bold;}
        .sub-text {text-align: center; font-size: 3rem !important;}
        .button-container {text-align: center;}
        .custom-button {
            background-color: #1E88E5;
            color: white;
            padding: 12px 24px;
            font-size: 1.2rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .custom-button:hover {background-color: #1565C0;}
    </style>
""", unsafe_allow_html=True)
# Custom CSS to improve aesthetics
st.markdown("""
    <style>
        .block-container {padding-top: 2rem !important;}
        .main-title {text-align: center; font-size: 7rem !important; font-weight: bold;}
        .sub-text {text-align: center; font-size: 3rem !important;}
        .button-container {text-align: center;}
        .custom-button {
            background-color: #1E88E5;
            color: white;
            padding: 12px 24px;
            font-size: 1.2rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .custom-button:hover {background-color: #1565C0;}
    </style>
""", unsafe_allow_html=True)

# Get the uploaded image path
image_path = "https://plus.unsplash.com/premium_photo-1733306679049-88a8bf1c2411?q=80&w=1954&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

# YouTube video URL
video_url = "https://www.youtube-nocookie.com/embed/16AbSxpRFJo?si=jJvUcV684O6nFWmg?autoplay=1&mute=1&loop=1&controls=0"

# Custom CSS for styling with enhanced fade-out animation
st.markdown("""
    <style>
        .title-container {
            position: relative;
            width: 100%;
            text-align: center;
            animation: fadeOut 5s forwards;
        }
        .title-container img {
            width: 100%;
            border-radius: 20px;
        }
        .overlay-text {
            position: absolute;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        .main-title {
            font-size: 64px !important;
            font-weight: bold;
            margin: 0;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        .sub-text {
            font-size: 32px !important;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            margin-top: 10px;
        }
        .video-container {
            width: 100%;
            margin: 0 auto;
        }
        @keyframes fadeOut {
            0% { 
                opacity: 1; 
                visibility: visible;
                max-height: 1000px; /* Large initial max-height */
            }
            90% { 
                opacity: 1; 
                visibility: visible;
                max-height: 1000px;
            }
            100% { 
                opacity: 0; 
                visibility: hidden;
                max-height: 0;
                padding: 0;
                margin: 0;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Display Title Section with Overlay
st.markdown(f"""
    <div class="title-container">
        <img src="{image_path}" alt="Fleet Optimization Image">
        <div class="overlay-text">
            <p class="main-title">🍃CarbonWise🍃</p>
            <p class="sub-text">Optimizing Fleet Operations with AI-Powered Efficiency</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Add YouTube video
st.markdown(f"""
    <div class="video-container">
        <iframe 
            width="100%" 
            height="600px" 
            src="{video_url}" 
            frameborder="0" 
            allow="autoplay; encrypted-media" 
            allowfullscreen
        ></iframe>
    </div>
""", unsafe_allow_html=True)


# About Section with Image and Text in Two Columns
st.markdown("""
    <style>
        .about-container {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #DBE5EA;
            padding: 15px;
            border-radius: 20px;
            margin: 30px 0;
        }
        .about-text {
            flex: 1;
            padding: 20px;
            text-align: left;
        }
        .about-title {
            font-size: 42px;
            font-weight: bold;
            color: #1565C0;
            margin-bottom: 10px;
        }
        .about-description {
            font-size: 20px;
            color: #0F4662;
            line-height: 1.6;
        }
        .highlight {
            color: #0F4662;
            font-weight: bold;
        }
        .about-image {
            flex: 1;
            text-align: center;
        }
        .about-image img {
            width: 100%;
            border-radius: 10px;
        }
        @media (max-width: 768px) {
            .about-container {
                flex-direction: column;
                text-align: center;
            }
            .about-text {
                text-align: center;
                margin-top: 20px;
            }
        }
    </style>

    <div class="about-container">
        <div class="about-image">
            <img src="https://plus.unsplash.com/premium_photo-1681074963670-2110c58f4c24?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Sustainable Fleet">
        </div>
        <div class="about-text">
            <h2 class="about-title">🔍 About Us</h2>
            <p class="about-description">
                At <span class="highlight">Carbon Wise</span>, we empower businesses to optimize fleet operations, 
                reducing <span class="highlight">costs</span> and minimizing <span class="highlight">carbon emissions</span>. 
                Our AI-driven approach transforms logistics companies into 
                <span class="highlight">greener, smarter, and more efficient</span> enterprises.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Key Features Section
st.header("🚛 Why Choose Carbon Wise?")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://plus.unsplash.com/premium_photo-1661935334659-a4f95e515c3b?q=80&w=2061&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)
    st.subheader("⚡ Smart Fleet Transition")
    st.write("Seamlessly shift towards **electric and low-emission** vehicles.")

with col2:
    st.image("https://images.unsplash.com/photo-1581092786450-7ef25f140997?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)
    st.subheader("📊 AI-Powered Optimization")
    st.write("Advanced **multi-criteria decision algorithms** for cost & emission reduction.")

with col3:
    st.image("https://plus.unsplash.com/premium_photo-1661934344726-6bc1a604575b?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)
    st.subheader("🌍 Sustainability at Scale")
    st.write("Reduce your carbon footprint while maintaining operational efficiency.")

# How It Works Section
st.markdown("""
    <style>
        .hiw-container {
            background: #DBE5EA;
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
        }
        .hiw-title {
            font-size: 42px;
            font-weight: bold;
            color: #1565C0;
            text-align: center;
            margin-bottom: 30px;
        }
        .hiw-steps {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 20px;
        }
        .hiw-step {
            flex: 1 1 200px;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .hiw-step:hover {
            transform: translateY(-5px);
        }
        .step-number {
            font-size: 28px;
            font-weight: bold;
            color: #1E88E5;
            margin-bottom: 10px;
        }
        .step-title {
            font-size: 22px;
            font-weight: bold;
            color: #0F4662;
            margin-bottom: 10px;
        }
        .step-description {
            font-size: 16px;
            color: #0F4662;
            line-height: 1.5;
        }
        .step-icon {
            font-size: 48px;
            text-align: center;
            margin-bottom: 15px;
        }
        @media (max-width: 768px) {
            .hiw-steps {
                flex-direction: column;
            }
        }
    </style>

    <div class="hiw-container">
        <h2 class="hiw-title">⚙️ How It Works?</h2>
        <div class="hiw-steps">
            <div class="hiw-step">
                <div class="step-icon">🔍</div>
                <div class="step-number">1️⃣</div>
                <div class="step-title">Fleet Data Analysis</div>
                <p class="step-description">We analyze your existing fleet and operational needs to establish a baseline.</p>
            </div>
            <div class="hiw-step">
                <div class="step-icon">🧠</div>
                <div class="step-number">2️⃣</div>
                <div class="step-title">AI-Driven Optimization</div>
                <p class="step-description">Our proprietary algorithms determine the optimal fleet mix for efficiency and sustainability.</p>
            </div>
            <div class="hiw-step">
                <div class="step-icon">🔄</div>
                <div class="step-number">3️⃣</div>
                <div class="step-title">Seamless Integration</div>
                <p class="step-description">We provide actionable insights for effortless implementation into your operations.</p>
            </div>
            <div class="hiw-step">
                <div class="step-icon">📈</div>
                <div class="step-number">4️⃣</div>
                <div class="step-title">Continuous Improvement</div>
                <p class="step-description">Optimize your fleet year after year for sustained efficiency and environmental impact.</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Testimonials Section
st.markdown("""
    <style>
        .testimonial-title {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
        }
        .testimonial-card {
            background: #DBE5EA;
            padding: 25px;
            border-radius: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .testimonial-text {
            font-style: italic;
            text-align: center;
            margin: 15px 0;
            color: #0F4662;
            line-height: 1.6;
            font-size: 14px;
        }
        .testimonial-author {
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 5px;
        }
        .testimonial-position {
            font-size: 12px;
            color: #0F4662;
            text-align: center;
        }
        .testimonial-image-container {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto 15px auto;
        }
    </style>
""", unsafe_allow_html=True)

# Testimonials Header
st.markdown("""
        <h2 class="testimonial-title">📝 What Our Clients Say</h2>
""", unsafe_allow_html=True)
st.divider()

# Create three columns for testimonials
col1, col2, col3 = st.columns(3)

# Testimonial 1
with col1:
    st.markdown("""
        <div class="testimonial-card">
            <div class="testimonial-image-container">
                <img src="https://images.unsplash.com/photo-1556157382-97eda2d62296?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" width="80" height="80" style="object-fit: cover; width: 100%; height: 100%;">
            </div>
            <p class="testimonial-text">"Carbon Wise helped us cut fleet costs by 23% and reduce emissions by 69%—a game changer!"</p>
            <p class="testimonial-author">John Doe</p>
            <p class="testimonial-position">Fleet Manager at Green Logistics</p>
        </div>
    """, unsafe_allow_html=True)

# Testimonial 2
with col2:
    st.markdown("""
        <div class="testimonial-card">
            <div class="testimonial-image-container">
                <img src="https://plus.unsplash.com/premium_photo-1690407617686-d449aa2aad3c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" width="80" height="80" style="object-fit: cover; width: 100%; height: 100%;">
            </div>
            <p class="testimonial-text">"The AI-powered route optimization alone saved us thousands in fuel costs each month. hehe hehe"</p>
            <p class="testimonial-author">Sarah Johnson</p>
            <p class="testimonial-position">COO at Express Delivery Services</p>
        </div>
    """, unsafe_allow_html=True)

# Testimonial 3
with col3:
    st.markdown("""
        <div class="testimonial-card">
            <div class="testimonial-image-container">
                <img src="https://images.unsplash.com/photo-1701096351544-7de3c7fa0272?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" width="80" height="80" style="object-fit: cover; width: 100%; height: 100%;">
            </div>
            <p class="testimonial-text">"As a sustainability officer, I appreciate how Carbon Wise balances environmental impact with business needs."</p>
            <p class="testimonial-author">Michael Chen</p>
            <p class="testimonial-position">Chief Sustainability Officer at EcoTrans</p>
        </div>
    """, unsafe_allow_html=True)

# Close the testimonial container
st.markdown("</div>", unsafe_allow_html=True)


# Center alignment using HTML & CSS
st.markdown(
    """
    <h1 style="text-align: center; font-size: 32px">📞 Get in Touch</h1>
    <p style="text-align: center;">Ready to optimize your fleet? Contact us today!</p>
    <p style="text-align: center;"><b>📧 Email:</b> contact@carbonwise.com  |  <b>📍 Location:</b> San Francisco, CA</p>
    """,
    unsafe_allow_html=True
)
# Minimalist Footer with Local Logo (Centered)
st.markdown('<hr style="border: 0.5px solid gray;">', unsafe_allow_html=True)

# Load & Center Image Properly
logo_path = "assets/logo.png"  # Ensure this is the correct path

col1, col2, col3 = st.columns([2, 1, 2])  # Creates 3-column layout
with col2:
    st.image(logo_path)  # Displays image in the center column

# Footer Details
st.markdown(
    """
    <p style="text-align: center; font-size: 12px; color: gray;">
        Driving sustainability with data-driven fleet optimization.
    </p>
    <p style="text-align: center; font-size: 12px; color: gray;">
        © 2025 CarbonWise. All rights reserved.
    </p>
    <p style="text-align: center; font-size: 12px;">
        <a href="https://linkedin.com/company/carbonwise" target="_blank" style="color: gray; text-decoration: none;">LinkedIn</a> |
        <a href="https://twitter.com/carbonwise" target="_blank" style="color: gray; text-decoration: none;">Twitter</a> |
        <a href="https://carbonwise.com" target="_blank" style="color: gray; text-decoration: none;">Website</a>
    </p>
    """,
    unsafe_allow_html=True
)

