// VerifyForm.js
import React from 'react';
import { Box, Button, Center } from '@chakra-ui/react';

const VerifyForm = ({ onVerify }) => {
    const handleVerify = () => {
        // Trigger verify action
        onVerify();
    };

    return (
        <Center>
            <Box>
                <Button onClick={handleVerify}>Verify</Button>
            </Box>
        </Center>
    );
};

export default VerifyForm;
