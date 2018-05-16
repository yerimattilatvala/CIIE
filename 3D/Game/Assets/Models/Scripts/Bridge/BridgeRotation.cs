using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BridgeRotation : MonoBehaviour {
	
	public GameObject c1,c2;
	public GameObject b1,b2;
	private bool update = true;

	void Start(){
		b2.SetActive (false);
	}
	// Update is called once per frame
	void FixedUpdate () {
		if(update)
		if (c1.activeSelf == false && c2.activeSelf == false) {
			b2.SetActive (true);
			b1.SetActive(false);
		}
	}
}
