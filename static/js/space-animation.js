// ============================================
// Hakimu 3D Space Animation - Solar System Sequence
// Three.js Cinematic Experience
// ============================================

class SolarSystemAnimation {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.planets = [];
        this.particles = [];
        this.clock = new THREE.Clock();
        this.animationState = 0; // 0: initial, 1: earth focus, 2: mars, 3-7: other planets
        this.transitionProgress = 0;
        this.mouseX = 0;
        this.mouseY = 0;
        
        this.init();
    }
    
    init() {
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupLights();
        this.createStars();
        this.createPlanets();
        this.setupEventListeners();
        this.animate();
    }
    
    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x030014); // Deep space color
    }
    
    setupCamera() {
        this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(0, 5, 25);
        this.camera.lookAt(0, 0, 0);
    }
    
    setupRenderer() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ReinhardToneMapping;
        this.renderer.toneMappingExposure = 1.2;
        
        // Add canvas to DOM
        const canvas = this.renderer.domElement;
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.zIndex = '-1';
        canvas.style.pointerEvents = 'none'; // Allow clicking through to website
        document.body.insertBefore(canvas, document.body.firstChild);
    }
    
    setupLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404060);
        this.scene.add(ambientLight);
        
        // Main directional light (sun)
        const sunLight = new THREE.DirectionalLight(0xffeedd, 1.5);
        sunLight.position.set(10, 10, 10);
        sunLight.castShadow = true;
        sunLight.receiveShadow = true;
        sunLight.shadow.mapSize.width = 1024;
        sunLight.shadow.mapSize.height = 1024;
        this.scene.add(sunLight);
        
        // Additional point lights for glow
        const pointLight1 = new THREE.PointLight(0x4466ff, 0.5, 30);
        pointLight1.position.set(-5, 2, 5);
        this.scene.add(pointLight1);
        
        const pointLight2 = new THREE.PointLight(0xff66aa, 0.3, 30);
        pointLight2.position.set(5, -2, 10);
        this.scene.add(pointLight2);
        
        // Ambient glow
        const ambientGlow = new THREE.PointLight(0x88aaff, 0.2, 50);
        ambientGlow.position.set(0, 0, 10);
        this.scene.add(ambientGlow);
    }
    
    createStars() {
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 3000;
        const starsPositions = new Float32Array(starsCount * 3);
        const starsColors = new Float32Array(starsCount * 3);
        
        for (let i = 0; i < starsCount * 3; i += 3) {
            // Distribute stars in a sphere
            const r = 50 + Math.random() * 50;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            starsPositions[i] = r * Math.sin(phi) * Math.cos(theta);
            starsPositions[i + 1] = r * Math.sin(phi) * Math.sin(theta);
            starsPositions[i + 2] = r * Math.cos(phi);
            
            // Random colors (mostly white/blue, some red)
            const colorVal = 0.5 + Math.random() * 0.5;
            starsColors[i] = Math.random() > 0.8 ? 1.0 : colorVal;
            starsColors[i + 1] = Math.random() > 0.8 ? 0.6 : colorVal;
            starsColors[i + 2] = Math.random() > 0.9 ? 1.0 : colorVal;
        }
        
        starsGeometry.setAttribute('position', new THREE.BufferAttribute(starsPositions, 3));
        starsGeometry.setAttribute('color', new THREE.BufferAttribute(starsColors, 3));
        
        const starsMaterial = new THREE.PointsMaterial({
            size: 0.2,
            vertexColors: true,
            transparent: true,
            blending: THREE.AdditiveBlending,
            sizeAttenuation: true
        });
        
        const stars = new THREE.Points(starsGeometry, starsMaterial);
        this.scene.add(stars);
        this.stars = stars;
    }
    
    createPlanets() {
        const planetData = [
            { name: 'Mercury', color: 0x8c8c8c, size: 0.3, distance: 4, speed: 0.02, glow: 0x888888 },
            { name: 'Venus', color: 0xe6b800, size: 0.35, distance: 5.5, speed: 0.015, glow: 0xffaa00 },
            { name: 'Earth', color: 0x2299ff, size: 0.4, distance: 7, speed: 0.01, glow: 0x4466ff },
            { name: 'Mars', color: 0xcc6600, size: 0.35, distance: 8.5, speed: 0.008, glow: 0xff5500 },
            { name: 'Jupiter', color: 0xd2b48c, size: 0.8, distance: 11, speed: 0.005, glow: 0xaa8866 },
            { name: 'Saturn', color: 0xe0c080, size: 0.7, distance: 13.5, speed: 0.004, glow: 0xccaa77 },
            { name: 'Uranus', color: 0x6cc0c0, size: 0.6, distance: 16, speed: 0.003, glow: 0x55aaaa },
            { name: 'Neptune', color: 0x4169e1, size: 0.6, distance: 18.5, speed: 0.002, glow: 0x3355bb }
        ];
        
        // Create orbits
        planetData.forEach(data => {
            this.createOrbit(data.distance);
        });
        
        // Create planets
        planetData.forEach((data, index) => {
            this.createPlanet(data, index);
        });
        
        // Position planets initially in a circle
        this.positionPlanetsInOrbit();
    }
    
    createOrbit(radius) {
        const points = [];
        const segments = 128;
        
        for (let i = 0; i <= segments; i++) {
            const angle = (i / segments) * Math.PI * 2;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            points.push(new THREE.Vector3(x, 0, z));
        }
        
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ color: 0x336699, transparent: true, opacity: 0.1 });
        const orbit = new THREE.LineLoop(geometry, material);
        this.scene.add(orbit);
    }
    
    createPlanet(data, index) {
        const geometry = new THREE.SphereGeometry(data.size, 64, 64);
        
        // Create material with slight emissive for glow
        const material = new THREE.MeshPhongMaterial({
            color: data.color,
            emissive: data.glow,
            emissiveIntensity: 0.1,
            shininess: 30,
            transparent: true,
            opacity: 1
        });
        
        const planet = new THREE.Mesh(geometry, material);
        planet.castShadow = true;
        planet.receiveShadow = true;
        
        // Add clouds/atmosphere for some planets
        if (data.name === 'Earth') {
            const cloudGeometry = new THREE.SphereGeometry(data.size * 1.01, 64, 64);
            const cloudMaterial = new THREE.MeshPhongMaterial({
                color: 0xffffff,
                transparent: true,
                opacity: 0.15,
                blending: THREE.AdditiveBlending,
                side: THREE.DoubleSide
            });
            const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
            planet.add(clouds);
        }
        
        // Add rings for Saturn
        if (data.name === 'Saturn') {
            const ringGeometry = new THREE.TorusGeometry(data.size * 1.5, 0.1, 16, 100);
            const ringMaterial = new THREE.MeshPhongMaterial({
                color: 0xc0a080,
                transparent: true,
                opacity: 0.4,
                side: THREE.DoubleSide
            });
            const ring = new THREE.Mesh(ringGeometry, ringMaterial);
            ring.rotation.x = Math.PI / 2;
            ring.rotation.z = 0.3;
            planet.add(ring);
        }
        
        // Store planet data
        planet.userData = {
            name: data.name,
            distance: data.distance,
            speed: data.speed,
            angle: (index / 8) * Math.PI * 2, // Distribute evenly
            originalSize: data.size,
            originalColor: data.color,
            glow: data.glow,
            index: index
        };
        
        this.planets.push(planet);
        this.scene.add(planet);
    }
    
    positionPlanetsInOrbit() {
        this.planets.forEach(planet => {
            const data = planet.userData;
            planet.position.x = Math.cos(data.angle) * data.distance;
            planet.position.z = Math.sin(data.angle) * data.distance;
            planet.position.y = 0;
        });
    }
    
    setupEventListeners() {
        window.addEventListener('resize', () => this.onWindowResize(), false);
        document.addEventListener('mousemove', (e) => this.onMouseMove(e), false);
    }
    
    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
    
    onMouseMove(event) {
        // Parallax effect - subtle movement based on mouse position
        this.mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
        this.mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
    }
    
    // Animation sequence methods
    updateAnimationState(deltaTime) {
        const time = Date.now() * 0.001;
        
        // Cycle through planets every 3 seconds
        this.animationState = Math.floor(time / 3) % 8;
        this.transitionProgress = (time % 3) / 3; // 0 to 1 over 3 seconds
        
        // Easing function for smooth transitions
        const easeInOut = t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        const easedProgress = easeInOut(this.transitionProgress);
        
        // Focus on current planet
        const targetPlanet = this.planets[this.animationState];
        if (targetPlanet) {
            // Smooth camera movement to focus on current planet
            const targetPos = targetPlanet.position.clone();
            targetPos.y += 1; // Slight height offset
            targetPos.multiplyScalar(1.5); // Zoom out a bit
            
            // Interpolate camera position
            this.camera.position.lerp(targetPos, 0.02);
            this.camera.lookAt(targetPlanet.position);
            
            // Glow effect on current planet
            this.planets.forEach((planet, idx) => {
                if (idx === this.animationState) {
                    // Current planet glows
                    planet.material.emissiveIntensity = 0.3 + Math.sin(time * 5) * 0.1;
                    planet.scale.setScalar(1 + Math.sin(time * 3) * 0.05);
                } else {
                    // Other planets fade out slightly
                    planet.material.emissiveIntensity = 0.1;
                    planet.scale.setScalar(1);
                }
            });
        }
        
        // Rotate planets
        this.planets.forEach(planet => {
            planet.rotation.y += 0.005;
            
            // Orbital movement
            if (planet.userData) {
                planet.userData.angle += planet.userData.speed * deltaTime * 10;
                planet.position.x = Math.cos(planet.userData.angle) * planet.userData.distance;
                planet.position.z = Math.sin(planet.userData.angle) * planet.userData.distance;
                
                // Slight vertical variation for depth
                planet.position.y = Math.sin(planet.userData.angle * 2) * 0.5;
            }
        });
        
        // Rotate stars slowly for parallax effect
        if (this.stars) {
            this.stars.rotation.y += 0.0001;
            this.stars.rotation.x += 0.00005;
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const deltaTime = this.clock.getDelta();
        
        // Update animation state
        this.updateAnimationState(deltaTime);
        
        // Mouse parallax effect
        this.camera.position.x += (this.mouseX * 2 - this.camera.position.x) * 0.01;
        this.camera.position.y += (-this.mouseY * 2 - this.camera.position.y) * 0.01;
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize animation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SolarSystemAnimation();
});