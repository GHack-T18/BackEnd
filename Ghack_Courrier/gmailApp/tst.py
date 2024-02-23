




import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Sample email dataset with labels
emails = [
    ("Important: Invoice Payment Reminder", "Finance"),
    ("Shipment Tracking Information", "Logistics"),
    ("Employee Benefits Update", "Human Resources"),
    ("Monthly Financial Report", "Finance"),
    ("HR Policy Changes", "Human Resources"),
    ("Urgent: Delivery Delay Notification", "Logistics"),
    ("Budget Approval Request", "Finance"),
    ("Warehouse Inventory Update", "Logistics"),
    ("Employee Performance Review", "Human Resources"),
]

# Preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    tokens = nltk.word_tokenize(text)  # Tokenize text
    stop_words = set(stopwords.words('english'))  # Get English stopwords
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    stemmer = PorterStemmer()  # Create stemmer object
    tokens = [stemmer.stem(word) for word in tokens]  # Stemming
    return ' '.join(tokens)

# Preprocess emails
preprocessed_emails = [(preprocess_text(email[0]), email[1]) for email in emails]

# Split dataset into features (X) and labels (y)
X = [email[0] for email in preprocessed_emails]
y = [email[1] for email in preprocessed_emails]

# Vectorize text using TF-IDF
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear')
classifier.fit(X_vectorized, y)

# Define mapping of categories to recipients
recipient_mapping = {
    'Finance': 'nadakouadri09@gmail.com',
    'Logistics': 'ln_kouadri@esi.dz',
    'Human Resources': 'dashevent2024@gmail.com'
}

# Function to send email
def send_email(sender_email, receiver_email, password, subject, body):
    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # SMTP server configuration (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Start TLS connection to SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to SMTP server
    server.login(sender_email, password)

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Quit SMTP server
    server.quit()

    print('Email sent successfully!')

# Function to transfer email to appropriate recipient
def transfer_email(email_content, category):
    recipient = recipient_mapping.get(category, 'default_recipient@example.com')
    sender_email = 'esigrad2023@gmail.com'  # Replace with your sender email
    password = 'NNNN'  # Replace with your sender email password
    subject = 'New Email'
    send_email(sender_email, recipient, password, subject, email_content)

# Process each email and transfer to appropriate recipient
for email_content, _ in emails:
    preprocessed_email = preprocess_text(email_content)
    email_vectorized = vectorizer.transform([preprocessed_email])
    category = classifier.predict(email_vectorized)[0]
    transfer_email(email_content, category)






import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email server configuration
email_user = 'esigrad2023@gmail.com'
email_password = ''
forward_to_email = 'ln_kouadri@esi.dz'  # Email address to forward messages to

# Connect to the email server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_user, email_password)
mail.select('inbox')

# Search for unread emails
result, data = mail.search(None, 'UNSEEN')

# Initialize SMTP connection to Gmail's SMTP server
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()
smtp_server.login(email_user, email_password)

# Iterate through unread emails
for num in data[0].split():
    result, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Check if the email message has a payload
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Extract text/plain parts
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    # Create a new email message for forwarding
    forwarded_email = MIMEMultipart()
    forwarded_email['From'] = email_user
    forwarded_email['To'] = forward_to_email
    forwarded_email['Subject'] = email_message['Subject']
    forwarded_email.attach(MIMEText(body, 'plain'))

    # Send the forwarded email
    smtp_server.sendmail(email_user, forward_to_email, forwarded_email.as_string())

# Close the connection
smtp_server.quit()
mail.close()
mail.logout()
