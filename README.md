# Pluto Hacks 2023
 Hackathon Project for Pluto Hacks 2023

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.x
- pip
- virtualenv (recommended)

## Setup

1. **Clone the repository**:

   \`\`\`bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   \`\`\`

2. **Set up a virtual environment** (optional but recommended):

   \`\`\`bash
   python -m venv myenv
   \`\`\`

   Activate the virtual environment:

   - On macOS and Linux:

     \`\`\`bash
     source myenv/bin/activate
     \`\`\`

   - On Windows:

     \`\`\`bash
     myenv\Scripts\activate
     \`\`\`

3. **Install the required packages**:

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Environment Variables**:

   This project uses environment variables for configuration. Make sure to set up the \`.env\` file in the root directory with your variables. An example \`.env\` could be:

   \`\`\`
   API_KEY=YOUR_OPENAI_API_KEY
   \`\`\`

   Replace \`YOUR_OPENAI_API_KEY\` with your actual API key.

## Running the Project

With the virtual environment activated and dependencies installed:

\`\`\`bash
python YOUR_MAIN_SCRIPT_NAME.py
\`\`\`

This will start the Flask server, and the API will be accessible at \`http://localhost:5000\`.

## Endpoints

Here are some of the main endpoints:

- **Start Recording**: \`POST /start_recording\`
- **Stop Recording**: \`POST /stop_recording\`
- **Play Audio**: \`GET /play_audio\`
- **Display Transcript**: \`GET /display_transcript\`
- **Display Summary**: \`GET /display_summary\`
- **Display Reminders**: \`GET /display_reminders\`
- **Translate**: \`GET /translate/<target_language>\`
- **Load Latest Recording**: \`GET /load_latest_recording\`

Refer to the source code or generated API documentation (if available) for detailed endpoint specifications.

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) (if available) before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
EOL