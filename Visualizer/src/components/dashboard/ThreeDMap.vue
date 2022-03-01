<template>
    <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
    Scene,
    Engine,
    ArcRotateCamera,
    MeshBuilder,
    Vector3,
    StandardMaterial,
    Color3,
    AxesViewer,
    DirectionalLight,
    Mesh,
    ActionManager,
    PointLight,
    ExecuteCodeAction,
    ShadowGenerator,
    HemisphericLight,
} from "babylonjs";
import { useSimulationStore } from "../../stores/simulation";

const simulationStore = useSimulationStore();

const canvas = ref(null);
let engine, scene, selectionLight, mainLight, hemisphereLight;

const x = simulationStore.dimensions.x;
const y = simulationStore.dimensions.y; // Direction of Sky
const z = simulationStore.dimensions.z;

const lengthOfAxis = Math.max(x, y, z) / 10;

const lineStep = 10; // Only draw an orientation line every x-th coordinate

const createScene = () => {
    const scene = new Scene(engine);
    scene.clearColor = Color3.FromHexString("#101010");

    const axes = new AxesViewer(scene, lengthOfAxis);
    axes.update(
        new Vector3(-x / 2, 0, -z / 2),
        new Vector3(1, 0, 0),
        new Vector3(0, 1, 0),
        new Vector3(0, 0, 1)
    );

    const target = new Vector3(0, (y / 4) * 3, 0);
    const camera = new ArcRotateCamera(
        "camera",
        -Math.PI / 2,
        Math.PI / 2.5,
        3,
        target,
        scene
    );
    camera.attachControl(canvas, true);
    camera.setTarget(target);
    camera.setPosition(new Vector3(-x, y * 2.5, -z));

    mainLight = new DirectionalLight(
        "directionalLight",
        new Vector3(-1, -1, -1),
        scene
    );
    mainLight.diffuse = new Color3.FromHexString("#ffffff");
    mainLight.specular = new Color3.FromHexString("#63e2b7");
    mainLight.groundColor = new Color3.FromHexString("#44ab87");
    mainLight.intensity = 1;
    mainLight.position.x = x / 2;
    mainLight.position.y = y / 2;
    mainLight.position.z = z / 2;

    hemisphereLight = new HemisphericLight(
        "HemiLight",
        new Vector3(0, 1, 0),
        scene
    );
    hemisphereLight.intensity = 0.5;

    const shadows = new ShadowGenerator(2048, mainLight);
    shadows.usePoissonSampling = true;

    const ground = MeshBuilder.CreateGround("ground", { width: x, height: z });
    const groundMaterial = new StandardMaterial(scene);
    groundMaterial.diffuseColor = new Color3.FromHexString("#313336");
    groundMaterial.alpha = 1;
    ground.material = groundMaterial;
    ground.receiveShadows = true;

    // Create orientation lines
    const lineAlpha = 0.025;

    for (let xi = 0; xi < x; xi += lineStep) {
        for (let yi = 0; yi < y; yi += lineStep) {
            const line = MeshBuilder.CreateLines(`line-x${xi}-y${yi}`, {
                points: [
                    new Vector3(xi - x / 2, yi, 0 - z / 2),
                    new Vector3(xi - x / 2, yi, z - z / 2),
                ],
            });
            line.alpha = lineAlpha;
            line.color = new Color3.White();
        }
    }
    for (let xi = 0; xi < x; xi += lineStep) {
        for (let zi = 0; zi < z; zi += lineStep) {
            const line = MeshBuilder.CreateLines(`line-x${xi}-z${zi}`, {
                points: [
                    new Vector3(xi - x / 2, 0, zi - z / 2),
                    new Vector3(xi - x / 2, y, zi - z / 2),
                ],
            });
            line.alpha = lineAlpha;
            line.color = new Color3.White();
        }
    }

    for (let yi = 0; yi < y; yi += lineStep) {
        for (let zi = 0; zi < z; zi += lineStep) {
            const line = MeshBuilder.CreateLines(`line-y${yi}-z${zi}`, {
                points: [
                    new Vector3(0 - x / 2, yi, zi - z / 2),
                    new Vector3(x - x / 2, yi, zi - z / 2),
                ],
            });
            line.alpha = lineAlpha;
            line.color = new Color3.White();
        }
    }

    // Create blockers
    const blockerMaterial = new StandardMaterial(scene);
    blockerMaterial.diffuseColor = new Color3.FromHexString("#313336");
    blockerMaterial.maxSimultaneousLights = 10;
    blockerMaterial.alpha = 1;

    simulationStore.environment.blockers.forEach((blocker) => {
        const cube = MeshBuilder.CreateBox(
            "box",
            {
                height: blocker.dimension.y,
                width: blocker.dimension.x,
                depth: blocker.dimension.z,
            },
            scene
        );
        cube.position.x = blocker.origin.x - x / 2;
        cube.position.y = blocker.origin.y + blocker.dimension.y / 2;
        cube.position.z = blocker.origin.z - z / 2;
        cube.material = blockerMaterial;
        cube.receiveShadows = true;
        shadows.getShadowMap().renderList.push(cube);
    });

    // Create selection  light
    selectionLight = new PointLight(
        "selection-light",
        new Vector3(0, 0, 0),
        scene
    );
    selectionLight.range = 0;
    selectionLight.intensity = 0;

    shadows.getShadowMap().refreshRate = 0;
    mainLight.autoUpdateExtends = false;

    return scene;
};

const activeMeshes = {};

const placeDrones = () => {
    // Remove unused meshes
    const activeUUIDs = simulationStore.activeAgentUUIDs;
    Object.entries(activeMeshes).forEach(([uuid, meshes]) => {
        if (!(uuid in activeUUIDs)) {
            meshes.forEach((mesh) => {
                mesh.dispose();
            });
            delete activeMeshes[uuid];
        }
    });

    // Push new meshes
    simulationStore.activeAgents.forEach((agent) => {
        if (!(agent.uuid in activeMeshes)) {
            // Draw path
            const points = agent.locations.map(
                (loc) => new Vector3(loc.x - x / 2, loc.y, loc.z - z / 2)
            );
            const line = MeshBuilder.CreateLines(`line-agent-${agent.uuid}`, {
                points,
            });
            line.alpha = 0.5;
            line.color = new Color3.FromHexString(agent.owner.color);

            // create Material
            const ownerMaterial = new StandardMaterial(scene);
            ownerMaterial.diffuseColor = new Color3.FromHexString(
                agent.owner.color
            );
            ownerMaterial.emissiveColor = new Color3.FromHexString(
                agent.owner.color
            );
            ownerMaterial.alpha = 1;

            // Draw drone
            const sphere = Mesh.CreateSphere(
                `sphere-agent-${agent.uuid}`,
                16,
                1,
                scene
            );
            sphere.material = ownerMaterial;
            sphere.isPickable = true;
            sphere.actionManager = new ActionManager(scene);

            sphere.actionManager.registerAction(
                new ExecuteCodeAction(ActionManager.OnPickTrigger, () => {
                    selectionLight.position.x = current_loc.x - x / 2;
                    selectionLight.position.y = current_loc.y;
                    selectionLight.position.z = current_loc.z - z / 2;
                    selectionLight.diffuse = new Color3.FromHexString(
                        agent.owner.color
                    );
                    selectionLight.specular = new Color3.FromHexString(
                        agent.owner.color
                    );
                    selectionLight.range = y*2;
                    selectionLight.intensity = 2;
                    mainLight.intensity = 0.1;
                    hemisphereLight.intensity = 0.1;
                })
            );

            activeMeshes[agent.uuid] = [line, sphere];
        }

        // Update sphere position
        const current_loc = agent.locations.find(
            (loc) => loc.t === simulationStore.tick
        );
        const sphere = activeMeshes[agent.uuid][1];

        sphere.position.x = current_loc.x - x / 2;
        sphere.position.y = current_loc.y;
        sphere.position.z = current_loc.z - z / 2;
    });
};

simulationStore.$subscribe(() => {
    placeDrones();
});

onMounted(() => {
    engine = new Engine(canvas.value, true, {
        preserveDrawingBuffer: true,
        stencil: true,
    });

    scene = createScene();
    placeDrones();

    // run the render loop
    engine.runRenderLoop(() => {
        scene.render();
    });

    // the canvas/window resize event handler
    window.addEventListener("resize", function () {
        engine.resize();
    });
});
</script>

<style scoped>
canvas {
    width: 100%;
    height: 750px;
    outline: none;
    -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
