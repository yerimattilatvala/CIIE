using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InteractObjects : MonoBehaviour {

    public GameObject OpenMsg;
	public GameObject CloseMsg;
    public GameObject Paper;
    public GameObject text;

    void Start()
    {
        OpenMsg.SetActive(false);
		CloseMsg.SetActive(false);
        text.SetActive(false);
        Paper.SetActive(false);
      

    }

	/* 

*/


    void OnTriggerStay(Collider other)
	{

		if (other.CompareTag ("Player")) {
			if (Paper.activeInHierarchy == false) {
				OpenMsg.SetActive (true);
				if (OpenMsg.activeInHierarchy == true && Input.GetButtonDown ("Use")) {

					Debug.Log ("Open Text");
					Paper.SetActive (true);
					text.SetActive (true);
					OpenMsg.SetActive (false);

				}
			}
			/*else {
				OpenMsg.SetActive (false);
				CloseMsg.SetActive (true);
				if (CloseMsg.activeInHierarchy == true && Input.GetButtonDown ("Quit")) {

					Debug.Log ("Close Text");
					Paper.SetActive (false);
					text.SetActive (false);
					CloseMsg.SetActive (false);
				}
			}
			*/

		}
	}

    
    private void Update()
    {
        
		if (Paper.activeInHierarchy == true){
			CloseMsg.SetActive (true);
			if (Input.GetButtonDown("Quit"))
               {
                   Debug.Log("Close Text");
					Paper.SetActive (false);
					text.SetActive (false);
					CloseMsg.SetActive (false);
               }
		}
    }
    

    void OnTriggerExit()
    {
        OpenMsg.SetActive(false);
    }

}
