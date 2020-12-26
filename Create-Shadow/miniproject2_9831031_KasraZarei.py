from matplotlib import image
import matplotlib.pyplot
import numpy


def create_new_image():
    input_address = input('Enter image address: ')
    image_data = image.imread(input_address)
    input_image = image_data.shape

    output_image = numpy.zeros((input_image[0], int(1.2 * input_image[1]), input_image[2]), dtype='uint8')

    for i in range(0, input_image[0]):
        output_image[i] = [255, 255, 255]

    for i in range(input_image[0]):
        for j in range(input_image[1]):
            if image_data[i][j][0] < 235 or image_data[i][j][1] < 235 or image_data[i][j][2] < 235:
                new_size = (0.05 * i) + j
                output_image[i][int(new_size)] = [90, 90, 90]

    for i in range(input_image[0]):
        for j in range(input_image[1]):
            if image_data[i][j][0] < 235 or image_data[i][j][1] < 235 or image_data[i][j][2] < 235:
                output_image[i][j] = image_data[i][j]

    matplotlib.pyplot.imshow(output_image)
    matplotlib.pyplot.show()


create_new_image()
