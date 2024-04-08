// RegisterForm.js
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

    const handleRegister = async () => {
        setSubmitting(true);
        try {
            const formData = new FormData();

            // Convert base64 to Blob
            const blob = await fetch(capturedImage).then((res) => res.blob());

            // Append Blob to FormData with correct content type
            formData.append('photo', blob, 'photo.jpg');

            // Make axios call
            const response = await axios.post(`https://127.0.0.1:8000/register?name=${name}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Handle response if needed
            console.log(response.data);

            // Call parent function to handle registration
            onRegister(name);
        } catch (error) {
            // Handle error
            console.error('Error occurred:', error);
        } finally {
            setSubmitting(false);
        }
    };

    const capture = () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setPhotoCaptured(true);
        setCapturedImage(imageSrc);
    };

    const resetCapture = () => {
        setPhotoCaptured(false);
        setCapturedImage(null);
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
               <HStack>
                {photoCaptured && (
                    <Button mt={4} colorScheme="blue" onClick={handleRegister} isLoading={submitting}>
                        {submitting ? 'Submitting...' : 'Submit'}
                    </Button>
                )}
                {!photoCaptured ? (
                    <Button mt={4} colorScheme="teal" onClick={capture}>
                        Capture
                    </Button>
                ) : (
                    <Button mt={4} colorScheme="red" onClick={resetCapture}>
                        Reset
                    </Button>
                )}
               </HStack>
            </Box>
        </Center>
    );
};

export default RegisterForm;
