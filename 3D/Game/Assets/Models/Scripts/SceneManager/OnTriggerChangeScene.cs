using UnityEngine;

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
				guiObject.SetActive (false);
				DontDestroyOnLoad (GameObject.FindGameObjectWithTag("Canvas"));
				DontDestroyOnLoad (other.gameObject);
				DontDestroyOnLoad (Camera.main.gameObject);
				SceneManager.LoadScene(sceneIndex);
				other.transform.position = new Vector3 (22.0f, -3.6f, 5.0f);
            }
            
        }
    }
    
    void OnTriggerExit(){
        guiObject.SetActive(false);
    }

}
