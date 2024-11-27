try:
    import qrcode
    import matplotlib.pyplot as plt
except:
    from os import system as cmd
    cmd("pip install qrcode[pil] matplotlib")
    import qrcode
    import matplotlib.pyplot as plt

def generate_qr_with_text(data, text_line1, text_line2, output_file="output.png"):
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
    fig, ax = plt.subplots(figsize=(5, 6))  # Adjust the size of the figure

    # Add the QR code to the plot
    ax.imshow(qr.make_image(fill_color="black", back_color="white"), cmap="gray")
    ax.axis('off')  # Hide the axes

    # Add the text below the QR code
    ax.text(0.5, -0.15, text_line1, ha='center', va='top', fontsize=20, transform=ax.transAxes)
    ax.text(0.5, -0.25, text_line2, ha='center', va='top', fontsize=20, transform=ax.transAxes)

    # Adjust layout to ensure the text is visible and properly spaced
    plt.subplots_adjust(top=1, bottom=0.1, left=0, right=1)  # Adjust bottom to leave space for text
    plt.tight_layout(pad=2)  # Tight layout to avoid cutting off text

    # Save the image
    plt.savefig(output_file, format="png", dpi=300)
    plt.close()  # Close the plot

    print(f"QR Code saved as {output_file}")

# Example usage
data = "https://example.com"
text_line1 = "Visit our website"
text_line2 = "Scan the QR code"
generate_qr_with_text(data, text_line1, text_line2, "qr_code_with_text_matplotlib.png")