import tensorflow as tf

def preprocess(file_path, ftype = 'str'):
    # Read in image from file path
    if ftype == 'str': 
        byte_img = tf.io.read_file(file_path)
    elif ftype == 'byte':
        byte_img = file_path
    else:
        raise ValueError("Invalid ftype: ftype can be 'str' or 'byte'")
    # Load in the image 
    img = tf.io.decode_jpeg(byte_img)
    
    # Preprocessing steps - resizing the image to be 100x100x3
    img = tf.image.resize(img, (100,100))
    # Scale image to be between 0 and 1 
    img = img / 255.0
    img = tf.reshape(img,[-1,100,100,3])
    # Return image
    return img