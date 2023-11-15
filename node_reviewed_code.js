// const OpenAI = require('openai');
// require('dotenv').config();
// const openai = new OpenAI({
//     apiKey: process.env.OPENAI_API_KEY
// })
// m = {1:"gpt-3.5-turbo", 2:"gpt-4-1106-preview"}
// async function chat(){
//     const chat = await openai.chat.completions.create({
//         model: m[1],
//         messages: [{role: "user", content: "What is 2x2?"}],
// })}
// let output = chat();
// console.log(output);



const {OpenAI} = require('openai');
const openai = require('openai');
require('dotenv').config();

const openai = new OpenAI({apiKey: process.env.OPENAI_API_KEY});
const m = {1:"gpt-3.5-turbo", 2:"gpt-4-1106-preview"}

async function stream_output_origin() {
  const stream = await openai.chat.completions.create({
    model: m[1],
    messages: [{ role: 'user', content: 'Say this is a test' }],
    stream: true,
  });
  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}

async function automated_parse_call_origin() {
  const runner = client.beta.chat.completions
    .runFunctions({
      model: m[1],
      messages: [{ role: 'user', content: 'How is the weather this week?' }],
      functions: [
        {
          function: getCurrentLocation,
          parameters: { type: 'object', properties: {} },
        },
        {
          function: getWeather,
          parse: JSON.parse, // or use a validation library like zod for typesafe parsing.
          parameters: {
            type: 'object',
            properties: {
              location: { type: 'string' },
            },
          },
        },
      ],
    })
    .on('message', (message) => console.log(message));

  const finalContent = await runner.finalContent();
  console.log();
  console.log('Final content:', finalContent);
}

async function getCurrentLocation_origin() {
  return 'Boston'; // Simulate lookup
}

async function getWeather_origin(location){
  // … do lookup …
  return { temperature, precipitation };
}

automated_parse_call();

stream_output();

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
