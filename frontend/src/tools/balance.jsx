import React, { useState, useEffect } from "react";
import socketIOClient from "socket.io-client";
const ENDPOINT = window.location.origin;

function BalanceWS() {
  const [response, setResponse] = useState("");

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on("bal", data => {
      setResponse(data);
    });
  }, []);

  return (
    <p>
      Balance: <p>{response}</p>
    </p>
  );
}

export default BalanceWS