import {sendMessage} from "../funcs/backend"
import React from "react";
import { useState } from "react";

export default function ChatInput({}) {
    const [text, setText] = useState('');
    return (
        <div>
            <input type="text" placeholder="Type your message here..." value={text} onChange={(e) => setText(e.target.value)} />
            <button onClick={() => sendMessage(text)}>Send</button>
        </div>
    )
}