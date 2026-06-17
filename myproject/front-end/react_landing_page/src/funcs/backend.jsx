import React from "react";
import { useState } from "react";

export const sendMessage = async (message) => {
    console.log("Message sent!");
    try {
        const res = await fetch("http://localhost:5000/api/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        return data.response;
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

export const messageListner = (message) => {
    console.log(message);
}