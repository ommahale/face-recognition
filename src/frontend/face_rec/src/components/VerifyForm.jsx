
// VerifyForm.js
import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Box, Button, Center, Image, HStack } from '@chakra-ui/react';

const VerifyForm = () => {
    const webcamRef = useRef(null);
    const [photoCaptured, setPhotoCaptured] = useState(false);
    const [capturedImage, setCapturedImage] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    const capture = () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setPhotoCaptured(true);
        setCapturedImage(imageSrc);
    };

    const resetCapture = () => {
        setPhotoCaptured(false);
        setCapturedImage(null);
    };

    const handleVerify = async () => {
        setSubmitting(true);
        try {
            const formData = new FormData();

            // Convert base64 image to JPEG format
            const canvas = document.createElement('canvas');
            const image = document.createElement('img'); // Create image element
            image.src = capturedImage;
            image.onload = function () {
                canvas.width = image.width;
                canvas.height = image.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(image, 0, 0, image.width, image.height);
                canvas.toBlob(async function (blob) {
                    // Append converted blob to FormData with correct content type
                    formData.append('photo', blob, 'photo.jpg');

                    // Make axios call
                    await axios.post('http://127.0.0.1:8000/evaluate', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                    // Handle response if needed
                    console.log('Verification successful');
                }, 'image/jpeg');
            };

        } catch (error) {
            // Handle error
            console.error('Error occurred:', error);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <Center>
            <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md">
                {!photoCaptured ? (
                    <Webcam audio={false} ref={webcamRef} />
                ) : (
                    <Image src={capturedImage} alt="Captured" maxWidth="100%" />
                )}

                <HStack>
                    {photoCaptured ? (
                        <Button mt={4} colorScheme="blue" onClick={handleVerify} isLoading={submitting}>
                            {submitting ? 'Verifying...' : 'Verify'}
                        </Button>
                    ) : (
                        <Button mt={4} colorScheme="teal" onClick={capture}>
                            Capture
                        </Button>
                    )}
                    {photoCaptured && (
                        <Button mt={4} colorScheme="red" onClick={resetCapture}>
                            Reset
                        </Button>
                    )}
                </HStack>
            </Box>
        </Center>
    );
};

export default VerifyForm;
