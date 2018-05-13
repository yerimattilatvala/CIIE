﻿using UnityEngine;

using UnityEngine.SceneManagement;

public class OnTriggerChangeScene : MonoBehaviour {

    public GameObject guiObject;
    public int sceneIndex;
    
    void Start (){
        guiObject.SetActive(false);
        
    }

    
    void OnTriggerStay(Collider other){
        
        if (other.CompareTag("Player")){
            
            guiObject.SetActive(true);
            if (guiObject.activeInHierarchy == true && Input.GetButtonDown("Use")){
				DontDestroyOnLoad (other.gameObject);
				SceneManager.LoadScene(sceneIndex);
				//Scene scene = SceneManager.GetSceneByBuildIndex(sceneIndex);
				//SceneManager.MoveGameObjectToScene (other.gameObject, scene);

				other.transform.position = new Vector3 (27.0f, -2.0f, -23.0f);
            }
            
        }
    }
    
    void OnTriggerExit(){
        guiObject.SetActive(false);
    }

}
