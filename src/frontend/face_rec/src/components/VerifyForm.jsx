import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Box, Button, Center, Image, Text, HStack, Grid, GridItem } from '@chakra-ui/react';

const VerifyForm = () => {
    const webcamRef = useRef(null);
    const [photoCaptured, setPhotoCaptured] = useState(false);
    const [capturedImage, setCapturedImage] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [predictions, setPredictions] = useState(null);

    const capture = () => {
        const imageSrc = webcamRef.current.getScreenshot();
        setPhotoCaptured(true);
        setCapturedImage(imageSrc);
    };

    const resetCapture = () => {
        setPhotoCaptured(false);
        setCapturedImage(null);
        setPredictions(null); // Reset predictions
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
                    const response = await axios.post('http://127.0.0.1:8000/thread-evaluate', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                    // Handle response
                    setPredictions(response.data);
                    setSubmitting(false)
                }, 'image/jpeg');
            };

        } catch (error) {
            // Handle error
            console.error('Error occurred:', error);
        } finally {
            // setSubmitting(false);
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
                <Button mt={4} colorScheme={photoCaptured ? "blue" : "teal"} onClick={photoCaptured ? handleVerify : capture}>
                    {photoCaptured ? (submitting ? 'Verifying...' : 'Verify') : 'Capture'}
                </Button>
                {photoCaptured && (
                    <Button mt={4} colorScheme="red" onClick={resetCapture}>
                        Reset
                    </Button>
                )}
                </HStack>

                {/* Display predictions */}
                {predictions && (
                    <Grid mt={4} templateColumns="repeat(2, 1fr)" gap={4}>
                        {Object.keys(predictions).map((key) => (
                            <GridItem key={key}>
                                <Box p={4} borderWidth="1px" borderRadius="lg">
                                    <Text fontWeight="bold">{key}</Text>
                                    <Text>Prediction: {predictions[key].prediction !== null ? predictions[key].prediction : "null"}</Text>
                                    <Text>Confidence: {predictions[key].confidence !== null ? predictions[key].confidence : "null"}</Text> 
                                </Box>
                            </GridItem>
                        ))}
                    </Grid>
                )}
            </Box>
        </Center>
    );
};

export default VerifyForm;
