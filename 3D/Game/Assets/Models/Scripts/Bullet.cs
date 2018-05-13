using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Bullet : MonoBehaviour {

	[SerializeField]float speed;
	[SerializeField]float timeToLive;
	[SerializeField]float damage;
	private AudioSource audioSource;

	private float volLowRange = .5f;
	private float volHighRange = 1.0f;

	void Start(){
		Camera myCamera = Camera.main;

		audioSource = GetComponent<AudioSource>();
		//Para variar el sonido en cada disparo
		audioSource.pitch = Random.Range (volLowRange, volHighRange);
		audioSource.Play ();

		float x = Screen.width / 2;
		float y = Screen.height / 2;

		Ray castPoint = Camera.main.ScreenPointToRay(new Vector3(x, y, 0));

		RaycastHit[] hits;
		hits = Physics.RaycastAll(castPoint, Mathf.Infinity);
		List<RaycastHit> someList = new List<RaycastHit>(hits);

		someList.Sort ((v1, v2) => (v1.distance.CompareTo (v2.distance)));

		foreach (var hit in someList) {

			if (hit.distance > 2){
				this.transform.LookAt (hit.point);
				break;
			}
				
		}
			

		Destroy (gameObject, timeToLive);
	}

	void Update(){
		transform.Translate (Vector3.forward * speed * Time.deltaTime);
	}

	void OnTriggerEnter(Collider other){
		print ("Hit " + other.name);
	}
}
