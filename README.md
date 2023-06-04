![PyneCone Notion](https://github.com/TH-Activities/saturday-hack-night-template/assets/64391274/1e2cbdc1-829f-409a-8d13-03648d912472)


# Expandify
Are you running short of datasets which you need to train for your computer vision application?.Expandify offers a streamlined solution to transform and augment your image datasets for training purposes. By accepting a compressed zip file containing images and their corresponding annotations, Expandify harnesses the power of advanced image processing techniques to generate expanded datasets with ease.
## Team members
1. [Suryan](https://github.com/suryan-s)
2. [Arjun](https://github.com/arjunindia)
## Link to product walkthrough
<!-- [link to video](Link Here) -->
- Would be updated soon
## How it Works ?

![image](https://github.com/suryan-s/Expandify/assets/76394506/416062bb-2d55-4537-a98a-5801bbad337b)
![Screenshot 2023-06-04 234656](https://github.com/suryan-s/Expandify/assets/76394506/13ef130c-b793-427c-9f38-f7fe77a02250)
![Screenshot 2023-06-04 234724](https://github.com/suryan-s/Expandify/assets/76394506/10cf36f0-51e5-4e56-a316-3a10a5ad7364)
![Screenshot 2023-06-04 234753](https://github.com/suryan-s/Expandify/assets/76394506/3d52bb5e-25f5-4408-b84c-ce1b69fa3b65)

- When dataset is provided as zip file, the images could be augmented using different methds like flipping, blurring, brightening, shearing etc such that more sample images could be generated.
- Currently the project supports only YOLOV8 based dataset / annotations / labels.

## Libraries used
- Pynecone
- OpenCV
## How to configure

1. Make sure the zip file you provide to the app has the directory layout meant for YOLO format. i.e annotations must be in .txt files
2. The programs look for images and labels folder in the main zip extracted directory. Within that the individual train, test and valid folders are accessed.
## How to Run
To run Expandify, perform the following steps:

1. Open a terminal or command prompt.
2. Navigate to the Expandify project directory.
3. Execute the command `pc run` to start the application after setting up the environment using the requirements.txt.
5. Access the application through your web browser at http://localhost:3000.
