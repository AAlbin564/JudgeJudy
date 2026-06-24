import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import TextBox from './components/TextBox'
import ChatInput from './components/ChatInput'
import {sendMessage} from "./funcs/backend"

function App() {
  const [count, setCount] = useState(0)
  const [reply, setReply] = useState("")
  const [message, setMessage] = useState("")

  const handleSendMessage = async () => {
    const response = await sendMessage(message);
    console.log("Received response:", response);
    setReply(response);
  }

  return (
      <section className="screen">
        <div className="chatarea">
          <TextBox reply={reply} setReply={setReply}/>
          <ChatInput message={message} setMessage={setMessage} onSend={handleSendMessage}/>
        </div>
      </section>
  )
}

export default App
