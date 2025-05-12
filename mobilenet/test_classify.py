from classify_image import classify_image

result = classify_image("monkey.jpg")  # zameni sa jelom ili svinjom po potrebi

for label, prob in result:
    print(f"{label}: {prob*100:.2f}%")
