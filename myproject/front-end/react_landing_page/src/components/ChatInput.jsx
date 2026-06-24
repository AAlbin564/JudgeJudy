import {sendMessage} from "../funcs/backend"
import React from "react";
import { useState } from "react";

export default function ChatInput({ message, setMessage, onSend }) {
    return (
        <div>
            <input type="text" placeholder="Type your message here..." value={message} onChange={(e) => setMessage(e.target.value)} />
            <button onClick={onSend}>Send</button>
        </div>
    )
}