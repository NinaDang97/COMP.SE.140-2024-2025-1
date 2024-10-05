const express = require('express');
const { execSync } = require('child_process');

const app = express();
const PORT = 5002;

app.get('/', (req, res) => {
    const data = {
        IP_address: execSync("ifconfig | grep 'inet ' | awk '{print $2}' | head -n 1").toString().trim(),
        processes: execSync('ps -o pid,comm').toString().trim(),
        disk_space: execSync('df -h /').toString().trim(),
        uptime: execSync('uptime').toString().trim()
    };
    res.json(data);
});

app.listen(PORT, () => {
    console.log(`Service2 is listening on port ${PORT}`);
});