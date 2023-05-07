import splitfolders


# splitfolders.ratio("DermData", output="Test4",
#     seed=1337, ratio=(.8, .2), group_prefix=1, move=False)
splitfolders.ratio("DermData2", output="BigTest2",
    seed=1337, ratio=(.8, .1), group_prefix=1, move=False)

# import annotated_images

# To only split into training and validation set, set a tuple to `ratio`, i.e, `(.8, .2)`.
# annotated_images.split('DermData2/images/', output_dir='Test3', seed=1337, ratio=(.8, .2))
