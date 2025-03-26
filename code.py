import sqlite3
import cv2
from pyzbar.pyzbar import decode

# Initialize databaseq
def create_database():
    conn = sqlite3.connect("barcodes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add valid barcodes
def insert_barcode(barcode):
    conn = sqlite3.connect("barcodes.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO barcodes (barcode) VALUES (?)", (barcode,))
        conn.commit()
        print(f"Barcode {barcode} added successfully!")
    except sqlite3.IntegrityError:
        print("Barcode already exists!")
    conn.close()

# Check if barcode exists
def is_valid_barcode(barcode):
    conn = sqlite3.connect("barcodes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barcodes WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to scan barcode
def scan_barcode():
    cap = cv2.VideoCapture(0)  # Open webcam
    print("Scanning for barcode... Press 'q' to quit.")

    while True:
        _, frame = cap.read()
        barcodes = decode(frame)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            print(f"Scanned: {barcode_data}")

            if is_valid_barcode(barcode_data):
                print("✅ Valid Barcode")
            else:
                print("❌ Not Valid Barcode")

        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main Execution
if __name__== "_main_":
    create_database()  # Ensure database is set up
    
    # Add some sample barcodes
    insert_barcode("124567890128")
    insert_barcode("987654321")
    
    # Start scanning
scan_barcode()