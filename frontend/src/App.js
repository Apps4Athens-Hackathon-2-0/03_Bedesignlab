import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import logo_header from './logo_header.png';
import logo from './logo.png';

const API_URL = 'http://127.0.0.1:8000';

// Parse story text into main story and options
const parseStoryWithOptions = (storyText) => {
  if (!storyText) return { mainStory: '', option1: '', option2: '' };
  
  // Use regex to find ##1## and ##2## markers
  const option1Match = storyText.match(/##1##\s*(.+?)(?=##2##|$)/s);
  const option2Match = storyText.match(/##2##\s*(.+?)$/s);
  
  // Get main story (everything before first ##)
  const mainStoryMatch = storyText.match(/^(.+?)(?=##\d+##|$)/s);
  
  return {
    mainStory: mainStoryMatch ? mainStoryMatch[1].trim() : storyText.trim(),
    option1: option1Match ? option1Match[1].trim() : '',
    option2: option2Match ? option2Match[1].trim() : ''
  };
};

function App() {
  const [story, setStory] = useState(null);
  const [storyId, setStoryId] = useState(null);
  const [newsSummary, setNewsSummary] = useState('');
  const [userInput, setUserInput] = useState('');
  const [continuations, setContinuations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [choiceCount, setChoiceCount] = useState(0); // Track number of choices
  const [isStoryEnded, setIsStoryEnded] = useState(false); // Track if story has ended

  const generateStory = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/generate-story`);

      const parsedStory = parseStoryWithOptions(response.data.story);

      setStory(parsedStory);
      setStoryId(response.data.story_id);
      setNewsSummary(response.data.news_summary);
      setContinuations([]);
    } catch (error) {
      console.error('Error generating story:', error);
      alert('Error generating story. Check console for details.');
    }
    setLoading(false);
  };

  const continueStory = async () => {
    if (!userInput.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/continue-story`, {
        story_id: storyId,
        user_input: userInput
      });
      
      setContinuations([...continuations, {
        userInput: userInput,
        continuation: response.data.continuation
      }]);
      setUserInput('');
    } catch (error) {
      console.error('Error continuing story:', error);
      alert('Error continuing story. Check console for details.');
    }
    setLoading(false);
  };

  const handleOptionSelect = async (optionText) => {
    if (!optionText.trim()) return;
    
    const newChoiceCount = choiceCount + 1;
    setChoiceCount(newChoiceCount);
    setLoading(true);
    
    try {
      // Check if this is the 4th choice - generate ending
      if (newChoiceCount >= 4) {
        const response = await axios.post(`${API_URL}/api/continue-story`, {
          story_id: storyId,
          user_input: `${optionText}. Now provide a satisfying conclusion to the story. Wrap up all plot threads and provide a definitive ending.`
        });
        
        const parsedContinuation = parseStoryWithOptions(response.data.continuation);
        
        setContinuations([...continuations, {
          userInput: optionText,
          continuation: parsedContinuation.mainStory
        }]);
        
        // Clear options and mark story as ended
        setStory({
          mainStory: story.mainStory,
          option1: '',
          option2: ''
        });
        setIsStoryEnded(true);
        
      } else {
        // Normal continuation with options
        const response = await axios.post(`${API_URL}/api/continue-story`, {
          story_id: storyId,
          user_input: optionText
        });
        
        const parsedContinuation = parseStoryWithOptions(response.data.continuation);
        
        setContinuations([...continuations, {
          userInput: optionText,
          continuation: parsedContinuation.mainStory
        }]);
        
        // Update story with new options if they exist
        if (parsedContinuation.option1 && parsedContinuation.option2) {
          setStory({
            mainStory: story.mainStory,
            option1: parsedContinuation.option1,
            option2: parsedContinuation.option2
          });
        }
      }
      
    } catch (error) {
      console.error('Error continuing story:', error);
      alert('Error continuing story. Check console for details.');
    } finally {
      setLoading(false);
    }
  };
  
  const resetStory = () => {
    setStory(null);
    setStoryId(null);
    setContinuations([]);
    setNewsSummary('');
    setChoiceCount(0);
    setIsStoryEnded(false);
  };

  return (
    <div className="App">
      <header className="App-header">
          <img src={logo_header} alt="Wild athens logo" className="logo"/>           

          {story && (
            <button 
              onClick={resetStory}
              className="secondary-btn"
            >
              ΕΧΙΤ
            </button>
          )}        
      </header>

      <div className="container">
        {!story ? (
          <div className="start-section">
            <img src={logo} alt="Wild athens logo and name" className="logo"/>
            <button 
              onClick={generateStory} 
              disabled={loading}
              className="primary-btn"
            >
              {loading ? 'GENERATING...' : 'START YOUR JOURNEY'}
            </button>
          </div>
        ) : (
          <div className="story-section">
            <div className="news-box">
              <p className="news-summary">{newsSummary}</p>
            </div>

            <div className="story-box">
              <div className="story-content">
                <p className="main-story">{story.mainStory}</p>

                {continuations.map((cont, index) => (
                  <div key={index} className="continuation">
                    <div className="user-direction">
                      <span>&gt;</span> {cont.userInput}
                    </div>
                    <p>{cont.continuation}</p>
                  </div>
                ))}

                {/* Display "The End" if story is finished */}
                {isStoryEnded && (
                  <div className="story-end">
                    <p>THE END.</p>
                    <a href="bedesignlab.com"
                      className="primary-btn"
                    >
                      {loading ? 'PREPARING' : 'I WANT TO MAKE ATHENS WILDER'}
                    </a>
                  </div>
                )}

                {!isStoryEnded && story.option1 && story.option2 && (
                  <div className="story-options">
                    <button 
                      className="option-btn"
                      onClick={() => handleOptionSelect(story.option1)}
                      disabled={loading}
                    >
                      <span className="option-number">&gt;</span>
                      {story.option1}
                    </button>
                    <button 
                      className="option-btn"
                      onClick={() => handleOptionSelect(story.option2)}
                      disabled={loading}
                    >
                      <span className="option-number">&gt;</span>
                      {story.option2}
                    </button>
                  </div>
                )}
                                
              </div>
            </div>

            {/* <div className="input-section">
              <h3>✨ Continue the story:</h3>
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && continueStory()}
                placeholder="E.g., 'add a plot twist' or 'make it darker'"
                disabled={loading}
              />
              <button 
                onClick={continueStory} 
                disabled={loading || !userInput.trim()}
                className="secondary-btn"
              >
                {loading ? 'Writing...' : 'Continue Story'}
              </button>
            </div> */}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;