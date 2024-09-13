import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, Text, Table, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# Set up SQLite Database
DATABASE_URL = "sqlite:///videographer_profiles.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Create a table schema
profiles_table = Table(
    'profiles', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(50), nullable=False),
    Column('username', String(30), nullable=False, unique=True),
    Column('profile_picture', Text),
    Column('location', String(100)),
    Column('email', String(100), nullable=False),
    Column('phone', String(20)),
    Column('specialization', Text),
    Column('skills', Text),
    Column('experience_level', String(20)),
    Column('languages_spoken', String(100)),
    Column('portfolio_links', Text),
    Column('past_projects', Text),
    Column('camera_equipment', Text),
    Column('audio_equipment', Text),
    Column('lighting_equipment', Text),
    Column('editing_software', String(100)),
    Column('preferred_project_types', Text),
    Column('preferred_industries', Text),
    Column('availability_status', Text),
    Column('compensation', Text),
    Column('social_media_links', Text),
    Column('follower_count', String(20)),
    Column('privacy_settings', String(30)),
    Column('notification_preferences', Text)
)

metadata.create_all(engine)

# Set up sessionmaker for ORM
Session = sessionmaker(bind=engine)
session = Session()

# Set page title and description
st.set_page_config(page_title="Videographer Profile Registration", layout="centered")
st.title("Videographer Profile Registration")
st.write("Fill out the form below to register as a videographer and showcase your skills.")

# A. Personal Information
st.header("A. Personal Information")
full_name = st.text_input("Full Name", max_chars=50)
username = st.text_input("Username/Display Name", max_chars=30)
profile_picture = st.file_uploader("Upload Profile Picture", type=['jpg', 'png'])
location = st.text_input("Location (City, State/Province, Country)")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number (Optional)")

# B. Professional Information
st.header("B. Professional Information")
specialization = st.multiselect("Select Your Specialization", ["Event Videography", "Commercial Videography", "Music Videos", "Documentaries", "Social Media Content", "Corporate Videos", "Short Films", "Other"])
skills = st.multiselect("Select Your Skills", ["Camera Operation", "Drone Videography", "Video Editing", "Sound Recording", "Color Grading", "Lighting Setup", "Storyboarding"])
experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Professional", "Expert"])
languages_spoken = st.text_input("Languages Spoken (Optional)")

# C. Portfolio & Work Samples
st.header("C. Portfolio & Work Samples")
portfolio_links = st.text_area("Links to Portfolio (e.g., YouTube, Vimeo)", height=100)
past_projects = st.text_area("Describe Past Projects (Optional)", height=100)

# D. Equipment
st.header("D. Equipment")
camera_equipment = st.text_area("List of Camera Equipment", height=100)
audio_equipment = st.text_area("List of Audio Equipment (Optional)", height=100)
lighting_equipment = st.text_area("List of Lighting Equipment (Optional)", height=100)
editing_software = st.text_input("Video Editing Software")

# E. Collaboration Preferences
st.header("E. Collaboration Preferences")
preferred_project_types = st.multiselect("Preferred Project Types", ["Short Films", "Commercials", "Music Videos", "Corporate Videos", "Event Videos", "Social Media Content"])
preferred_industries = st.multiselect("Preferred Industries (Optional)", ["Entertainment", "Advertising", "Fashion", "Technology", "Education", "Other"])
availability_status = st.multiselect("Availability Status", ["Available Immediately", "Part-time Availability", "Full-time Availability"])
compensation = st.multiselect("Preferred Compensation", ["Hourly Rates", "Project-based Rates", "Monetary Payment", "Negotiable"])

# F. Social Media & Online Presence
st.header("F. Social Media & Online Presence")
social_media_links = st.text_area("Add Social Media Links (Optional)", height=100)
follower_count = st.text_input("Followers/Subscribers Count (Optional)")


# H. Account Settings
st.header("H. Account Settings")
privacy_settings = st.selectbox("Profile Visibility", ["Public", "Only visible to potential clients"])
notification_preferences = st.multiselect("Notification Preferences", ["Email Notifications", "SMS Notifications", "In-app Notifications"])

# Submit button
if st.button("Submit"):
    # Prepare data for insertion
    new_profile = {
        'full_name': full_name,
        'username': username,
        'profile_picture': profile_picture.name if profile_picture else None,
        'location': location,
        'email': email,
        'phone': phone,
        'specialization': ', '.join(specialization),
        'skills': ', '.join(skills),
        'experience_level': experience_level,
        'languages_spoken': languages_spoken,
        'portfolio_links': portfolio_links,
        'past_projects': past_projects,
        'camera_equipment': camera_equipment,
        'audio_equipment': audio_equipment,
        'lighting_equipment': lighting_equipment,
        'editing_software': editing_software,
        'preferred_project_types': ', '.join(preferred_project_types),
        'preferred_industries': ', '.join(preferred_industries),
        'availability_status': ', '.join(availability_status),
        'compensation': ', '.join(compensation),
        'social_media_links': social_media_links,
        'follower_count': follower_count,
        'privacy_settings': privacy_settings,
        'notification_preferences': ', '.join(notification_preferences)
    }

    # Insert into database and check for unique username
    try:
        ins = profiles_table.insert().values(**new_profile)
        session.execute(ins)
        session.commit()
        st.success("Your videographer profile has been submitted successfully!")
    except IntegrityError:
        st.error("The username already exists. Please choose a different one.")
