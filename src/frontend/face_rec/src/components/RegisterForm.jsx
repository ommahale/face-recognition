import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Box, Button, Input, Center, Text, HStack } from '@chakra-ui/react';

const RegisterForm = ({ onRegister }) => {
    const webcamRef = useRef(null);
    const [name, setName] = useState('');
    const [photoCaptured, setPhotoCaptured] = useState(false);
    const [capturedImage, setCapturedImage] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');

    const handleRegister = async () => {
        setSubmitting(true);
        try {
            const formData = new FormData();

            // Convert base64 to Blob
            const blob = await fetch(capturedImage).then(res => res.blob());

            // Append Blob to FormData with correct content type
            formData.append('photo', blob, 'photo.jpg');

            // Make axios call
            const response = await axios.post(`http://127.0.0.1:8000/register?name=${name}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Handle response if needed
            console.log(response.data);

            // Notify user about successful API call
            setSuccessMessage('Registration successful!');

            // Call parent function to handle registration
            onRegister(name);
        } catch (error) {
            // Handle error
            console.error('Error occurred:', error);
        } finally {
            setSubmitting(false);
        }
    };

    const capture = async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        // Convert base64 to JPEG format
        const canvas = document.createElement('canvas');
        const image = new Image();
        image.src = imageSrc;
        await new Promise(resolve => {
            image.onload = function () {
                canvas.width = image.width;
                canvas.height = image.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(image, 0, 0);
                resolve();
            };
        });

        const jpegUrl = canvas.toDataURL('image/jpeg');
        setPhotoCaptured(true);
        setCapturedImage(jpegUrl);
    };

    const resetCapture = () => {
        setPhotoCaptured(false);
        setCapturedImage(null);
        setSuccessMessage('');
    };

    return (
        <Center>
            <Box p={4} borderWidth="1px" borderRadius="md" boxShadow="md">
                {!photoCaptured ? (
                    <Webcam audio={false} ref={webcamRef} />
                ) : (
                    <img src={capturedImage} alt="Captured" style={{ maxWidth: '100%' }} />
                )}
                <Input mt={4} placeholder="Enter your name" value={name} onChange={(e) => setName(e.target.value)} />
                <HStack mt={4}>
                    {photoCaptured && (
                        <Button colorScheme="blue" onClick={handleRegister} isLoading={submitting}>
                            {submitting ? 'Submitting...' : 'Submit'}
                        </Button>
                    )}
                    {!photoCaptured ? (
                        <Button colorScheme="teal" onClick={capture}>
                            Capture
                        </Button>
                    ) : (
                        <Button colorScheme="red" onClick={resetCapture}>
                            Reset
                        </Button>
                    )}
                </HStack>
                {successMessage && <Text mt={4} color="green.500">{successMessage}</Text>}
            </Box>
        </Center>
    );
};

export default RegisterForm;
