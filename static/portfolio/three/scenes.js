// ========================================
// Three.js 3D Scenes - Hakimu Portfolio
// ========================================

// ===== Interactive Robot Head (follows mouse) =====
function initRobotScene() {
    const container = document.getElementById('avatar-3d-placeholder');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404060);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(2, 5, 3);
    scene.add(dirLight);

    const backLight = new THREE.PointLight(0x4466ff, 0.5);
    backLight.position.set(-2, 1, -3);
    scene.add(backLight);

    // Create a simple robot head group
    const headGroup = new THREE.Group();

    // Head sphere
    const headGeo = new THREE.SphereGeometry(1, 32, 32);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xA855F7, emissive: 0x2D0B4A });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 0;
    headGroup.add(head);

    // Eyes
    const eyeGeo = new THREE.SphereGeometry(0.2, 16, 16);
    const eyeMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
    leftEye.position.set(-0.4, 0.3, 0.9);
    headGroup.add(leftEye);
    const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
    rightEye.position.set(0.4, 0.3, 0.9);
    headGroup.add(rightEye);

    // Pupils
    const pupilGeo = new THREE.SphereGeometry(0.1, 8, 8);
    const pupilMat = new THREE.MeshStandardMaterial({ color: 0x000000 });
    const leftPupil = new THREE.Mesh(pupilGeo, pupilMat);
    leftPupil.position.set(-0.4, 0.3, 1.1);
    headGroup.add(leftPupil);
    const rightPupil = new THREE.Mesh(pupilGeo, pupilMat);
    rightPupil.position.set(0.4, 0.3, 1.1);
    headGroup.add(rightPupil);

    // Antenna
    const antennaGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.8);
    const antennaMat = new THREE.MeshStandardMaterial({ color: 0xffaa00 });
    const antenna = new THREE.Mesh(antennaGeo, antennaMat);
    antenna.position.set(0, 1.4, 0);
    headGroup.add(antenna);
    const antennaBallGeo = new THREE.SphereGeometry(0.2);
    const antennaBall = new THREE.Mesh(antennaBallGeo, antennaMat);
    antennaBall.position.set(0, 1.8, 0);
    headGroup.add(antennaBall);

    scene.add(headGroup);
    headGroup.position.set(0, 0, 0);

    camera.position.set(0, 0.5, 5);
    camera.lookAt(0, 0.5, 0);

    // Mouse tracking
    const mouse = { x: 0, y: 0 };
    window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        // Smoothly rotate the head based on mouse
        const targetRotY = mouse.x * 0.5;
        const targetRotX = -mouse.y * 0.3;
        headGroup.rotation.y += (targetRotY - headGroup.rotation.y) * 0.1;
        headGroup.rotation.x += (targetRotX - headGroup.rotation.x) * 0.1;

        renderer.render(scene, camera);
    }

    animate();

    // Handle resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}

// Initialize all scenes when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // You can call other scene initializers here if needed
    if (document.getElementById('avatar-3d-placeholder')) {
        initRobotScene();
    }
});