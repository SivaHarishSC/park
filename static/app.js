document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('mapCanvas');
    const ctx = canvas.getContext('2d');
    const button = document.getElementById('startRosNodeButton');

    const homeDirectory = '/home/siva/test2/src/car';
    const mapImagePath = `${homeDirectory}/car/map1.png`;
    const carImagePath = `${homeDirectory}/picture/car.png`;

    const mapImage = new Image();
    const carImage = new Image();

    mapImage.src = mapImagePath;
    carImage.src = carImagePath;

    mapImage.onload = () => {
        ctx.drawImage(mapImage, 0, 0, canvas.width, canvas.height);
    };

    const modelToMap = (xPos, yPos) => {
        const yPosNew = xPos * 140;
        const xPosNew = yPos * 140;
        return { xPosNew, yPosNew };
    };

    const updateCarPosition = (xPos, yPos) => {
        const { xPosNew, yPosNew } = modelToMap(xPos, yPos);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(mapImage, 0, 0, canvas.width, canvas.height);
        ctx.drawImage(carImage, xPosNew, yPosNew, 80, 60);
    };

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to the server');
    });

    socket.on('update_position', (data) => {
        updateCarPosition(data.xPos, data.yPos);
    });

    button.addEventListener('click', () => {
        fetch('/start_ros_node', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    console.log('ROS node started successfully');
                } else {
                    console.error('Failed to start ROS node');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
