const http = require('http');
const url = require('url');

// Define your client ID and redirect URI
const clientId = 'amzn1.application-oa2-client.200c6fc078ff405180ea6b4e50710025';
//const redirectUri = 'http://localhost:5000/callback';
const redirectUri = 'https://www.google.com';


// Define the authentication endpoint
const authEndpoint = 'https://www.amazon.com/ap/oa';

// Define the parameters for the authentication request
const params = {
  client_id: clientId,
  redirect_uri: redirectUri,
  response_type: 'code',
  scope: 'profile', // Specify the scopes you need
};

// Create a server to handle incoming requests
const server = http.createServer((req, res) => {
  // Redirect all requests to the authentication URL
  const authUrl = `${authEndpoint}?${new URLSearchParams(params).toString()}`;
  res.writeHead(302, { 'Location': authUrl });
  res.end();
});

// Start the server and listen on port 3000 (or any port you prefer)
const port = 3000;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
