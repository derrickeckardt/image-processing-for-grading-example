    # c - gaussian
    gaussian_matrix = np.array([[0.003, 0.013, 0.022, 0.013, 0.003],
                                [0.013, 0.059, 0.097, 0.059, 0.013],
                                [0.022, 0.097, 0.159, 0.097, 0.022],
                                [0.013, 0.059, 0.097, 0.059, 0.013],
                                [0.003, 0.013, 0.022, 0.013, 0.003]])
    # print(timeit(lambda: convolute3(im,box_blur_matrix_dict), number = 1))
    # print(timeit(lambda: im.filter(ImageFilter.Kernel((3,3),[1,1,1,1,1,1,1,1,1],9)), number =1))
