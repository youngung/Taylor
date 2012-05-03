c$$$  program for finding shear rate for the given gamma (for F2Py)
c$$$  It basically takes granular stress and Schmid tensor to calculate the
c$$$  resolved shear stress and, subsequently, shear strain on each of the
c$$$  slip systems
      
      subroutine eachgrain(
     $     gamma_dot0, nss, nsd,
     $     crss, schmid, stress_gr,
     $     gamma_dot)

c     $     gamma_dot0,          ! gamma_dot0 is reference
c     $     nss                  ! number of slip systems
c     $     nsd                  ! number of stress dimension (I'd expect 6)
      
c     $     crss,                ! CRSS is given
c     $     schmid,              ! Schmid tensor is given:
                                 ! resolve the external stress to slip system
c     $     stress_gr,           ! the given granular full tensorial stress (referred to SA)
c     $     gamma_dot            ! The resulting resolved shear strains on SS

      implicit None
      integer nss, nsd, iss, isd
      real*8 crss(nss), schmid(nss, nsd), stress_gr(nsd)
      real*8 gamma_dot0, rss
      real*8 gamma_dot(nss)

c$$$c     -- f2py block starts
c$$$cf2py intent(out, copy) gamma_dot
c$$$cf2py intent(hide), depend(crss) :: nss = shape(crss, 0)
c$$$cf2py intent(hide), depend(stress_gr) :: nsd = shape(stress_gr, 0)
c$$$cf2py intent(in) gamma_dot0, crss, schmid, stress_gr
c$$$c     -- f2py block ends
      
      do iss=1, nss             ! slip system index
         rss = 0.
         gamma_dot(iss) = 0.  
         do isd=1, nsd          ! stress component index
            rss = rss + schmid(iss, isd) * stress_gr(isd)
         enddo
c     gamma_dot is hardwired to be positive
         gamma_dot(iss) = abs(gamma_dot0 *
     $        (rss / crss(nss)) ** 20.)
      enddo

      return
      end subroutine









      
      subroutine wholegrains(
     $     slipsystems,         ! To get Schmid tensor for the given Euler angles
     $     crss,                ! CRSS for all slip systems of all grains.
     $     rotmat,              ! The rotation matrix (CA -> SA)
     $     stress_gr,           ! Stresses on the all grains (referred to CA)

     $     gamma_dot,           ! Gamma_dots on each slip systems of all grains.

     $     ngr,                 ! Number of grains
     $     nss,                 ! Number of slip system
     $     nsd                  ! Stress dimension
     $     )

      implicit None
      integer ngr, nss, nsd, igr, iss, isd, i, j

      real*8 slipsystems(nss, 2, 3)
      real*8 crss(ngr, nss)
      real*8 rotmat(ngr, 3, 3)
      real*8 stress_gr(ngr, nsd)
      real*8 gamma_dot(ngr, nss)
      real*8 schmid_(nss, nsd)

      real*8 dum1(3), dum2(3)
      real*8 sn(3), sb(3)

c     -- f2py block starts
cf2py intent(out, copy) gamma_dot
cf2py intent(in) slipsystems, crss, rotmat, stress_gr
cf2py intent(hide), depend(slipsystems) :: nss = shape(slipsystems,0)
cf2py intent(hide), depend(rotmat) :: ngr = shape(rotmat, 0)
cf2py intent(hide), depend(stress_gr) :: nsd = shape(stress_gr, 1)
c     -- f2py block ends

      do igr=1, ngr
c     Schmid Tensor (CA) calculation necessary
         do iss=1, nss          ! Slip systems
            do i = 1, 3
               sn(i) = slipsystems(iss,1, i) ! CA
               sb(i) = slipsystems(iss,2, i) ! CA
            enddo

c     convert the CA vectors into SA vectors

            do i = 1, 3
               dum1(i) = 0.
               dum2(i) = 0.                           
               do j = 1, 3
                  dum1(i) = dum1(i) + rotmat(igr, i, j) * sn(j)
                  dum2(i) = dum2(i) + rotmat(igr, i, j) * sb(j)
               enddo
            enddo
            sn = dum1(i)
            sb = dum2(i)
c     --------------------------------------

            do isd=1, nsd       ! Stress dimensions
               do i = 1, 3
c     Schmid tensor calculation (referred to Xtal axis) ---
                  
                  schmid_(iss, isd) = schmid_(iss, isd) +
     $                 (sn(i) * sb(j) + sn(j) * sb(i))/2.
c     -----------------------------------------------------
               enddo
            enddo               ! isd
         enddo                  ! iss

c$$$         call eachgrain(
c$$$     $        gamma_dot0 = 1.0, nss = nss, nsd = nsd,
c$$$     $        crss=crss(igr), schmid = schmid_,
c$$$     $        stress_gr = stress_gr(igr),
c$$$     $        gamma_dot = gamma_dot(igr)
c$$$     $        )
      enddo                     ! igr

      write(*,*) 'crss', crss(1,1)
      write(*,*) stress_gr(1,1)
      write(*,*) gamma_dot(1,1)

      return
      end subroutine
c     End of gammadot.for
