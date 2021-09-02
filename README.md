
# Detection of Unhealthy Brain Disease using MRI with Artificial Intelligence

In our work, we have not only detected the brain tumor but we also segmented that
where is tumor in the Human Brain. The task of detecting the position of the tumor in the body
of the patient is the starting point for medical treatment. Brain tumor detection in an early stage
can help to reduce the death rate in the medical field. The most common brain tumor is gliomas.
It is categorized as HGG (high-grade glioma) and LGG (low-grade glioma). By the use of MRI,
we get information on gliomas. For sub-regions and details of a tumor, the MRI has the
following sequence such as T1-weighted image, T1-weighted with gadolinium contrast
enhancement (t1gd), T2-weighted image, and fluid-attenuated inversion recovery- (FLAIR)
weighted image
## Acknowledgements

 First and foremost, we would like to express our gratitude to the University of Engineering and Technology, Lahore (UET) for providing complete project or study materials to make my research easier. As an undergraduate student, the wonderful atmosphere leads to my success. Second, we would like to thank our counsellor, Sir Zain Shabbir, who is also our project supervisor, for his continuous guidance and instruction. Sir Zain Shabbir has shared a lot of his research experience with us, which has inspired us to work on our project. Aside from that, we would like to thank all our colleagues, lecturers, technicians, and Uetians club members who helped make our project a success. It is greatly appreciated that they participated in the project's experimental phase. Finally, and most importantly, we would like to thank our family for all they've done. Throughout our undergraduate studies, they have supported us   in academia. We are thankful for their endless moral support. Their inspiration and encouragement have been at the center of my drive to learn and create
  
  
## Authors

- Ahmed Sanaullah
- Muniba kokab
- Noman Nosher
- Arslan Nasir
## Dataset for Classification
- kaggle dataset is used for brain tumor classification

## Dataset for Segmentation
We use BraTS 2018 data which consists of 210 HGG (High Grade Glioma) images and 75 
LGG (Low Grade Glioma) along with survival dataset for 163 patients. We use only HGG 
images 180 for training and 30 for testing. MRI images are categorized in following sequence 
i.e., T1-weighted image, T1-weighted with gadolinium contrast enhancement (t1gd), T2-
weighted image, and fluid-attenuated inversion recovery- (FLAIR) weighted image. Each 
image is a 3D image with size (240,240,155).
![Screenshot_1](https://user-images.githubusercontent.com/87497905/131785385-36f37ad5-5067-4dcc-8a48-eab8dba5f150.png)

## Architecture for Segmentation, U-Net
UNET architecture is named after its U like shape. This architecture [33] is inspired to deal 
with specifically biomedical image segmentation. Because in medical field, Large amount of 
data is not available easily. In case of large amount of data, neural networks can be trained for 
months to extract the features. 

![Screenshot_4](https://user-images.githubusercontent.com/87497905/131785547-058cd70c-839c-4bfe-8ed4-91898ebc37db.png)

## Segmentation of four different classes of brain tumor

-![tumor_segmentation](https://user-images.githubusercontent.com/87497905/131783353-07d29f4e-f2e0-4043-a2c0-6063f072b749.jpg)
## Our model Classification Results

![Screenshot_6](https://user-images.githubusercontent.com/87497905/131785539-28772a7b-db08-4001-95d7-0c219505841f.png)
## Our model Segmentation Results

![Screenshot_7](https://user-images.githubusercontent.com/87497905/131785543-55fbd1bf-d2a5-433d-9227-ada3aa7375ed.png)
## python files description
- Tumor_classification.py will work for 2d images and give results of binary classification whether tumor is present or not.
- Other two python files named Tumor segmentation are used for segmentation of 3d input images.


  
## Deployment in Google colab

To deploy this project on Google colab.
Run the above files in colab environment. No libraries are required for this to install. 

## Deployment in local Environment

To deploy this project on local machine. Install packages in requirement file and run the following commands.
- sudo python filename
- sudo python3 filename
## Further Readings
-Download thesis.pdf file from repository
