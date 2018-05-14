using System;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

namespace UnityStandardAssets.Characters.ThirdPerson
{
	[RequireComponent(typeof (ThirdPersonCharacter))]
	public class ThirdPersonUserControl : MonoBehaviour
	{
		private ThirdPersonCharacter m_Character; // A reference to the ThirdPersonCharacter on the object
		private Transform m_Cam;                  // A reference to the main camera in the scenes transform
		private Vector3 m_CamForward;             // The current forward direction of the camera
		private Vector3 m_Move;
		private bool m_Jump;                      // the world-relative desired move direction, calculated from the camForward and user input.
		private bool m_Block;
		private GameObject ScapeBar;
		private GameObject ScapeBar2;
		private GameObject ScapeBar2Original;
		private GameObject t1;
		private GameObject t2;
		private int count = 0;
		private int currentLife = 0;
		private int lastCurrentLife = 0;
		private Vector3 positionEnemy;
		private int c2 = 0;

		private void Start()
		{
			m_Block = false;
			ScapeBar = GameObject.Find ("Zombie/CanvasCatch/ScapeBar");
			ScapeBar2 = GameObject.Find ("Zombie/CanvasCatch/ScapeBarRed");
			ScapeBar2Original = ScapeBar2;
			t1 = GameObject.Find ("Zombie/CanvasCatch/TextoScape");
			t2 = GameObject.Find ("Zombie/CanvasCatch/TextoScape2");
			ScapeBar.gameObject.SetActive (false);
			ScapeBar2.gameObject.SetActive (false);
			ScapeBar2Original.gameObject.SetActive (false);
			t1.gameObject.SetActive (false);
			t2.gameObject.SetActive (false);

			// get the transform of the main camera
			if (Camera.main != null)
			{
				m_Cam = Camera.main.transform;
			}
			else
			{
				Debug.LogWarning(
					"Warning: no main camera found. Third person character needs a Camera tagged \"MainCamera\", for camera-relative controls.", gameObject);
				// we use self-relative controls in this case, which probably isn't what the user wants, but hey, we warned them!
			}

			// get the third person character ( this should never be null due to require component )
			m_Character = GetComponent<ThirdPersonCharacter>();
		}

		public void setCharacterLife(int life){
			lastCurrentLife = life;
		}

		public void setCharacterCurrentLife(int life){
			currentLife = life;
		}

		public void setPositionEnemy(Vector3 pos){
			positionEnemy = pos;
		}

		private void Update()
		{
			if (!m_Jump)
			{
				m_Jump = CrossPlatformInputManager.GetButtonDown("Jump");
			}
		}

		public bool Stop(){
			if ((currentLife<(lastCurrentLife-30)) && count<20)
				m_Block = true;
			else
				m_Block = false; 

			return m_Block;
		}

		// Fixed update is called in sync with physics
		private void FixedUpdate()
		{
			Debug.Log (m_Block);
			Debug.Log (count);

			// read inputs
			float h = CrossPlatformInputManager.GetAxis("Horizontal");
			float v = CrossPlatformInputManager.GetAxis("Vertical");
			bool crouch = Input.GetKey(KeyCode.C);

			// calculate move direction to pass to character
			if (m_Cam != null)
			{
				// calculate camera relative direction to move:
				m_CamForward = Vector3.Scale(m_Cam.forward, new Vector3(1, 0, 1)).normalized;
				m_Move = v*m_CamForward + h*m_Cam.right;
			}
			else
			{
				// we use world-relative directions in the case of no main camera
				m_Move = v*Vector3.forward + h*Vector3.right;
			}
			#if !MOBILE_INPUT
			// walk speed multiplier
			if (Input.GetKey(KeyCode.LeftShift)) m_Move *= 0.5f;
			#endif

			// pass all parameters to the character control script
			if (m_Block) {
				if (count >= 20) {
					m_Block = false;	
				}m_Move = new Vector3 (0, 0, 0);
				m_Character.Move (m_Move, crouch, false);
				ScapeBar.gameObject.SetActive (true);
				t1.gameObject.SetActive (true);
				t2.gameObject.SetActive (true);
				if (Input.GetKey (KeyCode.Return) == true) {
					if (count == 0) {
						ScapeBar2Original.gameObject.SetActive (true);
						count++;
					} else {
						ScapeBar2Original.transform.localScale = new Vector3 (count, 1, 1);
						count++;
					}

				}
				c2++;
			} else {
				count = 0;
				ScapeBar2Original = ScapeBar2;
                /*Esto no deberia ser false?*/
				ScapeBar2.gameObject.SetActive (true);
				ScapeBar2Original.gameObject.SetActive (false);
				ScapeBar.gameObject.SetActive (false);
				t1.gameObject.SetActive (false);
				t2.gameObject.SetActive (false);
				m_Character.Move(m_Move, crouch, m_Jump);
				m_Jump = false;
			}
		}
	}
}
