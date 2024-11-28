try:
    import qrcode
    import matplotlib.pyplot as plt
except:
    from os import system as cmd
    cmd("pip install qrcode[pil] matplotlib")
    import qrcode
    import matplotlib.pyplot as plt
import textwrap
import sqlite3

def generate_qr_with_text(data, text_line1, text_line2, output_file="output.png"):
    # Function to wrap text
    def wrap_text(text, max_width):
        wrapped = textwrap.fill(text, width=max_width)
        return wrapped

    # Create the QR code
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 6))  # Increased figure height to make space for text

    # Add the QR code to the plot
    ax.imshow(qr.make_image(fill_color="black", back_color="white"), cmap="gray")
    ax.axis('off')  # Hide the axes

    # Wrap the text
    max_width = 30  # Maximum number of characters per line
    wrapped_text1 = wrap_text(text_line1, max_width)
    wrapped_text2 = wrap_text(text_line2, max_width)

    # Add the wrapped text below the QR code
    ax.text(0.5, -0.1, wrapped_text1, ha='center', va='top', fontsize=16, transform=ax.transAxes)
    ax.text(0.5, -0.25, wrapped_text2, ha='center', va='top', fontsize=16, transform=ax.transAxes)

    # Adjust layout to ensure the text is visible and properly spaced
    plt.subplots_adjust(top=1, bottom=0.3, left=0, right=1)  # Adjust bottom to leave space for text
    plt.tight_layout(pad=2)  # Tight layout to avoid cutting off text

    # Save the image
    plt.savefig(output_file, format="png", dpi=300)
    plt.close()  # Close the plot

    print(f"QR Code saved as {output_file}")

db = sqlite3.connect("data.db")
cursor = db.cursor()

cursor.execute("SELECT id, type, ep FROM ids")
ids = cursor.fetchall()

for id1, bktype, ep in ids:
    cursor.execute("SELECT title FROM books WHERE id=?", (bktype,))
    title = cursor.fetchone()[0]
    print(id1, title, "("+str(ep)+")")
    generate_qr_with_text(id1, id1, f"{title} ({str(ep)})", f"output/{id1}.png")

# generate_qr_with_text(data, text_line1, text_line2, "qr_code_with_text_matplotlib.png")