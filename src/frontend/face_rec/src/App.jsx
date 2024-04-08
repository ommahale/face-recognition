// App.js
import React, { useState } from 'react';
import { ChakraProvider, Tab, TabList, TabPanel, TabPanels, Tabs } from '@chakra-ui/react';
import RegisterForm from './components/RegisterForm';
import VerifyForm from './components/VerifyForm';

const App = () => {
  const [registered, setRegistered] = useState(false);
  const [name, setName] = useState('');

  const handleRegister = (userName) => {
    setName(userName);
    setRegistered(true);
  };

  const handleVerify = () => {
    // Perform verification action here
    console.log('Verifying...');
  };

  return (
    <ChakraProvider>
      <Tabs>
        <TabList>
          <Tab>Register</Tab>
          <Tab>Verify</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <RegisterForm onRegister={handleRegister} />
          </TabPanel>
          <TabPanel>
            <VerifyForm onVerify={handleVerify} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </ChakraProvider>
  );
};

export default App;
