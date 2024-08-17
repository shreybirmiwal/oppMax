import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, orderBy, onSnapshot } from "firebase/firestore";


const firebaseConfig = {
    apiKey: "AIzaSyCR93rCmjROYrk8oclD0BHWjgdgIJwmDkM",
    authDomain: "oppmax2-b6131.firebaseapp.com",
    projectId: "oppmax2-b6131",
    storageBucket: "oppmax2-b6131.appspot.com",
    messagingSenderId: "745825345996",
    appId: "1:745825345996:web:8768c206d35170d4ad7d69"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db, collection, query, orderBy, onSnapshot };