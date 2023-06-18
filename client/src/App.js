import { useState } from 'react';
import './App.css';
import axios from 'axios';
import {
  ChakraProvider,
  Container,
  VStack,
  Button,
  Heading,
  Text,
  Input,
  Spinner,
} from '@chakra-ui/react'

const BACKEND_URL = "http://localhost:8000";

function App() {
  const [prompt, setPrompt] = useState('');
  const handleChange = (event) => setPrompt(event.target.value);
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true);
    axios
    .get(BACKEND_URL + "/papers?prompt=" + prompt)
    .then((res) => {
      console.log(res);
      setOutput(res.data);
    })
    .catch((err) => {
      console.log(err);
    })
    .finally(() => {
      setLoading(false);
    });
  }

  const addLineBreaks = (text) => {
    const split = text.split("\n");
    return split.map((s) => <>{s}<br/></>)
  }

  return (
    <ChakraProvider>
      <Heading size="lg" textAlign="center" margin="20px">
        ResearchGPT
      </Heading>
      <Heading size="md" textAlign="center">
        Built using LlamaIndex
      </Heading>
      <Container maxW="600px" marginTop="40px">
        <VStack>
          <Text>
            Enter research topics or concepts you're looking for in papers
          </Text>
          <Input
            value={prompt}
            onChange={handleChange}
            placeholder="e.g. 'What are some papers about reinforcement learning in music?'"
            size="md"
          />
          <Button size="lg" onClick={handleSearch}>
            Search
          </Button>
          {loading ? <Spinner size="lg" marginTop="50px" /> : <Text>{output ? addLineBreaks(output) : 'No answer found.'}</Text>}
        </VStack>
      </Container>
    </ChakraProvider>
  );
}

export default App;
