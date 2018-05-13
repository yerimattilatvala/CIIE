using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StepScript : MonoBehaviour {

	AudioSource audioSource;

	// Use this for initialization
	void Start () {
		audioSource = GetComponent<AudioSource> ();
	}
	
	void OnCollisionEnter(Collision collision){
		print ("Floor");
		if (collision.gameObject.tag == "Terrain") {
			audioSource.Play ();
		}
	}
}
