using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InteractObjects : MonoBehaviour {

    public GameObject guiObject;
    public GameObject Paper;
    public GameObject text;

    void Start()
    {
        guiObject.SetActive(false);
        text.SetActive(false);
        Paper.SetActive(false);
      

    }


    void OnTriggerStay(Collider other)
    {

        if (other.CompareTag("Player"))
        {

            guiObject.SetActive(true);
            if (guiObject.activeInHierarchy == true && Input.GetButtonDown("Use"))
            {

                Debug.Log("Open");
                Paper.SetActive(true);
                text.SetActive(true);

            }
        }

    }

    /*
    private void Update()
    {
        
               if (Paper.activeInHierarchy == true && Input.GetButtonDown("Use"))
               {
                   Debug.Log("Close");
                   Paper.SetActive(false);
                   text.SetActive(false);
               }
    }*/

    void OnTriggerExit()
    {
        guiObject.SetActive(false);
    }

}
