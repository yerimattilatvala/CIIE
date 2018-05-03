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
                SceneManager.LoadScene(sceneIndex);
            }
            
        }
    }
    
    void OnTriggerExit(){
        guiObject.SetActive(false);
    }

}
